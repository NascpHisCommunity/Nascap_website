// static/js/app.js
document.addEventListener("DOMContentLoaded", () => {
  /**
   * Lightweight utilities
   */
  const $$ = (id) => document.getElementById(id);

  // Simple HTML escaper (use text nodes instead of innerHTML where possible)
  const escapeText = (s) => (s == null ? "" : String(s));

  // Abort + timeout wrapper for fetch
  const fetchWithTimeout = (url, opts = {}, timeoutMs = 12000) => {
    const controller = new AbortController();
    const id = setTimeout(() => controller.abort(), timeoutMs);
    const merged = { ...opts, signal: controller.signal, credentials: "same-origin" };
    return fetch(url, merged).finally(() => clearTimeout(id));
  };

  // JSON fetch with retries + basic caching
  const memoryCache = new Map(); // url -> {ts, data}
  async function getJSON(url, { retries = 1, cacheTtlMs = 60_000 } = {}) {
    const cached = memoryCache.get(url);
    const now = Date.now();
    if (cached && now - cached.ts < cacheTtlMs) return cached.data;

    let lastErr;
    for (let attempt = 0; attempt <= retries; attempt++) {
      try {
        const res = await fetchWithTimeout(url, { headers: { "Accept": "application/json" } });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        memoryCache.set(url, { ts: now, data });
        return data;
      } catch (e) {
        lastErr = e;
        // exponential backoff: 200ms, 400ms
        if (attempt < retries) await new Promise(r => setTimeout(r, 200 * (2 ** attempt)));
      }
    }
    throw lastErr;
  }

  // Date formatter (uses browser locale)
  const fmtDate = (isoStr) => {
    if (!isoStr) return "";
    const d = new Date(isoStr);
    return new Intl.DateTimeFormat(undefined, { year: "numeric", month: "short", day: "2-digit" }).format(d);
  };

  // Set container busy state and messages
  function setBusy(container, busy = true) {
    if (!container) return;
    container.setAttribute("aria-busy", String(busy));
  }
  function setMessage(container, msg) {
    if (!container) return;
    container.innerHTML = "";
    const p = document.createElement("p");
    p.className = "text-muted mb-0";
    p.textContent = msg;
    container.appendChild(p);
  }

  /**
   * Generic fetch + render
   */
  async function fetchAndRender(url, containerId, renderFn) {
    const container = $$(containerId);
    if (!container) {
      console.error(`Container #${containerId} not found`);
      return;
    }
    setBusy(container, true);
    // Lightweight skeleton
    container.innerHTML = "";
    const skel = document.createElement("div");
    skel.className = "w-100 text-center py-3";
    skel.textContent = "Loading…";
    container.appendChild(skel);

    try {
      const data = await getJSON(url, { retries: 2, cacheTtlMs: 90_000 });
      container.innerHTML = "";
      renderFn(container, data);
    } catch (err) {
      console.error(`Error fetching ${url}:`, err);
      setMessage(container, "Sorry, this section failed to load.");
    } finally {
      setBusy(container, false);
    }
  }

  /**
   * File list (thumbnails)
   * file: { title, file_type, url, thumbnail_url? }
   */
  function renderFileList(container, files) {
    container.innerHTML = "";
    if (!Array.isArray(files) || files.length === 0) {
      return setMessage(container, "No files found.");
    }

    const ul = document.createElement("ul");
    ul.className = "list-unstyled";
    ul.setAttribute("role", "list");

    files.forEach((file) => {
      const li = document.createElement("li");
      li.className = "d-flex align-items-center mb-3";
      li.setAttribute("role", "listitem");

      const img = document.createElement("img");
      img.alt = escapeText(file.title || "file");
      img.loading = "lazy";
      img.decoding = "async";
      img.width = 100;
      img.style.height = "auto";
      img.className = "me-3 rounded";

      const type = String(file.file_type || "").toLowerCase();
      const thumbBase = "/static/images";
      if (type === "pdf") {
        img.src = `${thumbBase}/pdf_thumbnail.png`;
      } else if (type.includes("word") || type.includes("doc")) {
        img.src = `${thumbBase}/word_thumbnail.png`;
      } else if (type.includes("video") || type === "mp4") {
        img.src = file.thumbnail_url || `${thumbBase}/video_thumbnail.png`;
      } else if (type.includes("image") || /\.(png|jpe?g|gif|webp|svg)(\?|$)/i.test(file.url || "")) {
        img.src = file.thumbnail_url || file.url || `${thumbBase}/image_thumbnail.png`;
      } else {
        img.src = `${thumbBase}/file_thumbnail.png`;
      }
      img.onerror = () => { img.src = `${thumbBase}/file_thumbnail.png`; };

      const info = document.createElement("div");
      const titleEl = document.createElement("a");
      titleEl.href = file.url || "#";
      titleEl.className = "fw-semibold d-block";
      titleEl.textContent = escapeText(file.title || "Untitled");

      const meta = document.createElement("small");
      meta.className = "text-muted";
      meta.textContent = type ? `(${type})` : "";

      info.appendChild(titleEl);
      info.appendChild(meta);

      li.appendChild(img);
      li.appendChild(info);
      ul.appendChild(li);
    });

    container.appendChild(ul);
  }

  /**
   * Simple content list
   * content: { title, category? }
   */
  function renderContentList(container, contents) {
    container.innerHTML = "";
    if (!Array.isArray(contents) || contents.length === 0) {
      return setMessage(container, "No content found.");
    }
    const ul = document.createElement("ul");
    ul.className = "list-unstyled";
    ul.setAttribute("role", "list");

    contents.forEach((item) => {
      const li = document.createElement("li");
      li.setAttribute("role", "listitem");
      li.textContent = escapeText(item.title || "Untitled");
      if (item.category) {
        const cat = document.createElement("span");
        cat.className = "text-muted";
        cat.textContent = `  [Category: ${escapeText(item.category)}]`;
        li.appendChild(cat);
      }
      ul.appendChild(li);
    });
    container.appendChild(ul);
  }

  /**
   * Department components grid
   * component: { title, slug }
   */
  function renderDepartmentComponents(container, components) {
    container.innerHTML = "";
    if (!Array.isArray(components) || components.length === 0) {
      return setMessage(container, "No department components found.");
    }

    // Ensure proper list semantics for screen readers
    container.setAttribute("role", "list");

    const getAbbreviation = (title) => {
      if (!title) return "";
      // take first letters of up to three significant words
      const words = title
        .split(/[\s-]+/)
        .filter(Boolean)
        .slice(0, 3);
      return words.map(w => w[0]).join("").toUpperCase();
    };

    components.forEach((component) => {
      const a = document.createElement("a");
      a.href = `/department/${encodeURIComponent(component.slug || "")}/`;
      a.className = "text-decoration-none";

      const card = document.createElement("article");
      card.className = "d-flex flex-column flex-center m-3 p-3 rounded-3";
      card.style.flex = "0 0 30%";
      card.style.minWidth = "220px";
      card.setAttribute("role", "listitem");

      const symbolSpan = document.createElement("span");
      symbolSpan.className = "mb-3";
      // SVG added via DOM, no untrusted HTML
      const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
      svg.setAttribute("width", "48");
      svg.setAttribute("height", "48");
      svg.setAttribute("viewBox", "0 0 24 24");
      svg.setAttribute("fill", "none");
      const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
      circle.setAttribute("cx", "12");
      circle.setAttribute("cy", "12");
      circle.setAttribute("r", "10");
      circle.setAttribute("stroke", "currentColor");
      circle.setAttribute("stroke-width", "2");
      svg.appendChild(circle);
      symbolSpan.appendChild(svg);

      const infoDiv = document.createElement("div");
      infoDiv.className = "mb-0 text-center";

      const valueContainer = document.createElement("div");
      valueContainer.className = "fs-lg-2hx fs-2x fw-bolder text-white d-flex justify-content-center";
      const valueDiv = document.createElement("div");
      valueDiv.className = "min-w-70px";
      valueDiv.textContent = getAbbreviation(component.title);
      valueContainer.appendChild(valueDiv);

      const labelSpan = document.createElement("span");
      labelSpan.className = "text-gray-600 fw-bold fs-5 lh-0 d-block";
      labelSpan.textContent = escapeText(component.title || "Untitled");

      infoDiv.appendChild(valueContainer);
      infoDiv.appendChild(labelSpan);
      card.appendChild(symbolSpan);
      card.appendChild(infoDiv);
      a.appendChild(card);
      container.appendChild(a);
    });
  }

  /**
   * News + Events Carousel
   * item: { title, body, created_at }
   */
  function renderNewsEventsCarousel(newsAndEvents) {
    const carouselInner = $$("news-events-carousel-inner");
    if (!carouselInner) {
      console.error('Carousel container "news-events-carousel-inner" not found.');
      return;
    }
    carouselInner.innerHTML = "";

    const items = Array.isArray(newsAndEvents) ? [...newsAndEvents] : [];
    items.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));

    items.forEach((item, idx) => {
      const wrapper = document.createElement("div");
      wrapper.className = "carousel-item" + (idx === 0 ? " active" : "");

      const inner = document.createElement("div");
      inner.className = "d-block w-100 text-center p-3";

      const h3 = document.createElement("h3");
      h3.className = "text-white";
      h3.textContent = escapeText(item.title || "Untitled");

      // First sentence extraction (strip rudimentary HTML)
      const plain = String(item.body || "").replace(/<[^>]+>/g, " ");
      const firstSentence = (plain.match(/[^.!?]*[.!?]/) || [plain.trim()])[0].trim();

      const p = document.createElement("p");
      p.className = "text-white";
      p.textContent = escapeText(firstSentence);

      const h5 = document.createElement("h5");
      h5.className = "text-white";
      h5.textContent = fmtDate(item.created_at);

      inner.appendChild(h3);
      inner.appendChild(p);
      inner.appendChild(h5);
      wrapper.appendChild(inner);
      carouselInner.appendChild(wrapper);
    });

    if (items.length === 0) {
      const empty = document.createElement("div");
      empty.className = "carousel-item active";
      const inner = document.createElement("div");
      inner.className = "d-block w-100 text-center p-3";
      const p = document.createElement("p");
      p.className = "text-white mb-0";
      p.textContent = "No news or events at the moment.";
      inner.appendChild(p);
      empty.appendChild(inner);
      carouselInner.appendChild(empty);
    }
  }

  /**
   * Endpoints map
   */
  const endpoints = [
    // Files
    { url: "/api/files/",                         containerId: "file-list",                     render: renderFileList },
    { url: "/api/top-reports-files/",             containerId: "top-reports-files-list",        render: renderFileList },
    { url: "/api/top-publications-files/",        containerId: "top-publications-files-list",   render: renderFileList },
    { url: "/api/top-resources-files/",           containerId: "top-resources-files-list",      render: renderFileList },
    { url: "/api/top-analysis-files/",            containerId: "top-analysis-files-list",       render: renderFileList },
    { url: "/api/all-reports-files-by-slug/",     containerId: "all-reports-files-list",        render: renderFileList },
    { url: "/api/all-publications-files/",        containerId: "all-publications-files-list",   render: renderFileList },
    { url: "/api/all-resources-files/",           containerId: "all-resources-files-list",      render: renderFileList },
    { url: "/api/top-video-files/",               containerId: "top-video-files-list",          render: renderFileList },
    { url: "/api/top-image-files/",               containerId: "top-image-files-list",          render: renderFileList },
    { url: "/api/all-video-files/",               containerId: "all-video-files-list",          render: renderFileList },
    { url: "/api/all-image-files/",               containerId: "all-image-files-list",          render: renderFileList },

    // Content
    { url: "/api/latest-news-events/",            containerId: "latest-news-events-list",       render: renderContentList },
    { url: "/api/department-contents/",           containerId: "department-contents-list",      render: renderDepartmentComponents },
    { url: "/api/top-blogs-contents/",            containerId: "top-blogs-contents-list",       render: renderContentList },
    { url: "/api/top-projects-contents/",         containerId: "top-projects-contents-list",    render: renderContentList },
    { url: "/api/all-news-contents/",             containerId: "all-news-contents-list",        render: renderContentList },
    { url: "/api/all-events-contents/",           containerId: "all-events-contents-list",      render: renderContentList },
    { url: "/api/all-blogs-contents/",            containerId: "all-blogs-contents-list",       render: renderContentList },
    { url: "/api/all-projects-contents/",         containerId: "all-projects-contents-list",    render: renderContentList },
  ];

  // Fire requests
  endpoints.forEach(({ url, containerId, render }) => {
    fetchAndRender(url, containerId, render);
  });

  // News + Events merged carousel
  (async function fetchAndRenderNewsEvents() {
    try {
      const [newsData, eventsData] = await Promise.all([
        getJSON("/api/top-news-contents/",  { retries: 2, cacheTtlMs: 60_000 }),
        getJSON("/api/top-events-contents/", { retries: 2, cacheTtlMs: 60_000 }),
      ]);
      const merged = [...(newsData || []), ...(eventsData || [])];
      renderNewsEventsCarousel(merged);
    } catch (err) {
      console.error("Error fetching merged news/events:", err);
      // Optional: fall back to latest combined endpoint if you have one
      try {
        const combined = await getJSON("/api/latest-news-events/", { retries: 1, cacheTtlMs: 60_000 });
        renderNewsEventsCarousel(combined || []);
      } catch (e2) {
        const carouselInner = $$("news-events-carousel-inner");
        if (carouselInner) {
          carouselInner.innerHTML = `<div class="carousel-item active"><div class="d-block w-100 text-center p-3"><p class="text-white mb-0">Unable to load news and events.</p></div></div>`;
        }
      }
    }
  })();
});