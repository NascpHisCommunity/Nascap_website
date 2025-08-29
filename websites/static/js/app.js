// static/js/app.js
document.addEventListener('DOMContentLoaded', () => {
  /**
   * Generic function to fetch data from a URL and render it.
   *
   * @param {string} url - The API endpoint.
   * @param {string} containerId - The id of the DOM element where data will be rendered.
   * @param {Function} renderFunction - A function that accepts (container, data) and updates the DOM.
   */
  async function fetchAndRender(url, containerId, renderFunction) {
    try {
      console.log(`Fetching data from ${url}...`);
      console.log(`Rendering data into container with id "${containerId}"...`);
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      const data = await response.json();
      console.log(`Data from ${url}:`, data);
      const container = document.getElementById(containerId);
      if (container) {
        renderFunction(container, data);
      } else {
        console.error(`Container with id "${containerId}" not found.`);
      }
    } catch (error) {
      console.error(`Error fetching data from ${url}:`, error);
    }
  }

  /**
   * Render a list of file objects with thumbnails.
   * Assumes each file has properties: title, file_type, url, and optionally thumbnail_url.
   *
   * @param {HTMLElement} container - The container to render the file list.
   * @param {Array} files - The array of file objects.
   */
  function renderFileList(container, files) {
    container.innerHTML = ''; // Clear previous content
    if (Array.isArray(files) && files.length) {
      const ul = document.createElement('ul');
      files.forEach(file => {
        const li = document.createElement('li');
        li.style.marginBottom = '10px';
        li.style.display = 'flex';
        li.style.alignItems = 'center';

        // Create an image element for the thumbnail
        const img = document.createElement('img');
        img.alt = file.title;
        img.style.width = '100px';
        img.style.height = 'auto';
        img.style.marginRight = '10px';

        const type = file.file_type.toLowerCase();
        if (type === 'pdf') {
          img.src = '/static/images/pdf_thumbnail.png';
        } else if (type.includes('word')) {
          img.src = '/static/images/word_thumbnail.png';
        } else if (type.includes('video') || type === 'mp4') {
          img.src = file.thumbnail_url ? file.thumbnail_url : '/static/images/video_thumbnail.png';
        } else if (type.includes('image')) {
          // For images, if a thumbnail URL is provided, use it; otherwise, use the file's URL.
          img.src = file.thumbnail_url ? file.thumbnail_url : file.url;
        } else {
          // Generic file thumbnail
          img.src = '/static/images/file_thumbnail.png';
        }

        // Create a span element for file details
        const info = document.createElement('span');
        info.textContent = `${file.title} (${file.file_type})`;

        li.appendChild(img);
        li.appendChild(info);
        ul.appendChild(li);
      });
      container.appendChild(ul);
    } else {
      container.textContent = 'No files found.';
    }
  }

  /**
   * Render a list of content objects.
   * Assumes each content object has at least a 'title' property and optionally a 'category' property.
   *
   * @param {HTMLElement} container - The container to render the content list.
   * @param {Array} contents - The array of content objects.
   */
  function renderContentList(container, contents) {
    container.innerHTML = ''; // Clear previous content
    if (Array.isArray(contents) && contents.length) {
      const ul = document.createElement('ul');
      contents.forEach(content => {
        const li = document.createElement('li');
        li.textContent = content.title;
        if (content.category) {
          li.textContent += ` [Category: ${content.category}]`;
        }
        ul.appendChild(li);
      });
      container.appendChild(ul);
    } else {
      container.textContent = 'No content found.';
    }
  }

  /**
   * Render department components dynamically.
   * For each department component (from /api/department-contents/), create a clickable block that:
   * - Shows a placeholder SVG icon,
   * - Displays an abbreviation (computed from the title) in the "value" area,
   * - Displays the full title in a "label" area,
   * - Is wrapped in an <a> tag whose href links to a detail page (constructed from the component’s slug).
   *
   * @param {HTMLElement} container - The container to render the department components.
   * @param {Array} components - The array of department component objects.
   */
  function renderDepartmentComponents(container, components) {
    container.innerHTML = '';
    if (Array.isArray(components) && components.length) {
      components.forEach(component => {
        // Helper: Compute abbreviation (first letters of each word, up to 3 letters)
        const getAbbreviation = (title) => {
          if (!title) return '';
          const words = title.split(' ');
          let abbr = words.map(word => word.charAt(0)).join('');
          return abbr.substring(0, 3).toUpperCase();
        };

        // Build detail URL using the component's slug (adjust the URL pattern as needed)
        const detailUrl = `/department/${component.slug}/`;

        // Create anchor element wrapping the entire component.
        const a = document.createElement('a');
        a.href = detailUrl;
        a.style.textDecoration = 'none';

        // Create container div for the component.
        const div = document.createElement('div');
        div.className = 'd-flex flex-column flex-center m-3';
        div.style.flex = '0 0 30%'; // Approximately 3 per row

        // Create symbol span with a placeholder SVG icon.
        const symbolSpan = document.createElement('span');
        symbolSpan.className = 'svg-icon svg-icon-2tx svg-icon-white mb-3';
        symbolSpan.innerHTML = `<svg width="48" height="48" viewBox="0 0 24 24" fill="none">
                                    <circle cx="12" cy="12" r="10" stroke="black" stroke-width="2"></circle>
                                  </svg>`;

        // Create info div.
        const infoDiv = document.createElement('div');
        infoDiv.className = 'mb-0';

        // Create value div for the abbreviation.
        const valueContainer = document.createElement('div');
        valueContainer.className = 'fs-lg-2hx fs-2x fw-bolder text-white d-flex flex-center';
        const valueDiv = document.createElement('div');
        valueDiv.className = 'min-w-70px';
        valueDiv.setAttribute('data-kt-countup', 'false');
        valueDiv.textContent = getAbbreviation(component.title);
        valueContainer.appendChild(valueDiv);

        // Create label span for the full title.
        const labelSpan = document.createElement('span');
        labelSpan.className = 'text-gray-600 fw-bold fs-5 lh-0';
        labelSpan.textContent = component.title;

        // Append value and label to info div.
        infoDiv.appendChild(valueContainer);
        infoDiv.appendChild(labelSpan);

        // Append the symbol and info div to the container div.
        div.appendChild(symbolSpan);
        div.appendChild(infoDiv);

        // Append the container div into the anchor.
        a.appendChild(div);

        // Append the anchor to the main container.
        container.appendChild(a);
      });
    } else {
      container.textContent = 'No department components found.';
    }
  }

  /**
   * Render merged news and events into a single carousel.
   * Expects each item to have: title, body, and created_at.
   *
   * @param {Array} newsAndEvents - Array of news and event items.
   */
  function renderNewsEventsCarousel(newsAndEvents) {
    const carouselInner = document.getElementById('news-events-carousel-inner');
    if (!carouselInner) {
      console.error('Carousel container "news-events-carousel-inner" not found.');
      return;
    }
    carouselInner.innerHTML = '';

    // Sort by created_at descending
    newsAndEvents.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));

    newsAndEvents.forEach((item, index) => {
      // Extract the first sentence from the body.
      let firstSentence = item.body || '';
      const periodIndex = firstSentence.indexOf('.');
      if (periodIndex !== -1) {
        firstSentence = firstSentence.substring(0, periodIndex + 1);
      }
      const carouselItem = document.createElement('div');
      carouselItem.className = 'carousel-item' + (index === 0 ? ' active' : '');
      carouselItem.innerHTML = `
        <div class="d-block w-100 text-center">
          <h3 class="text-white">${item.title}</h3>
          <p class="text-white">${firstSentence}</p>
          <h5 class="text-white">${new Date(item.created_at).toLocaleDateString()}</h5>
        </div>
      `;
      carouselInner.appendChild(carouselItem);
    });
  }

  // Helper for fetch responses.
  function handleResponse(response) {
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return response.json();
  }

  /**
   * Fetch and render merged news and events for the carousel.
   */
  async function fetchAndRenderNewsEvents() {
    try {
      const [newsData, eventsData] = await Promise.all([
        fetch('/api/top-news-contents/').then(handleResponse),
        fetch('/api/top-events-contents/').then(handleResponse)
      ]);
      console.log('News data:', newsData);
      console.log('Events data:', eventsData);
      const mergedData = [...newsData, ...eventsData];
      renderNewsEventsCarousel(mergedData);
    } catch (error) {
      console.error('Error fetching news and events data:', error);
    }
  }

  // Define endpoints along with their container IDs and render functions.
  const endpoints = [
    // File endpoints
    { url: '/api/files/', containerId: 'file-list', render: renderFileList },
    { url: '/api/top-reports-files/', containerId: 'top-reports-files-list', render: renderFileList },
    { url: '/api/top-publications-files/', containerId: 'top-publications-files-list', render: renderFileList },
    { url: '/api/top-resources-files/', containerId: 'top-resources-files-list', render: renderFileList },
    { url: '/api/top-analysis-files/', containerId: 'top-analysis-files-list', render: renderFileList },
    { url: '/api/all-reports-files-by-slug/', containerId: 'all-reports-files-list', render: renderFileList },
    { url: '/api/all-publications-files/', containerId: 'all-publications-files-list', render: renderFileList },
    { url: '/api/all-resources-files/', containerId: 'all-resources-files-list', render: renderFileList },
    { url: '/api/top-video-files/', containerId: 'top-video-files-list', render: renderFileList },
    { url: '/api/top-image-files/', containerId: 'top-image-files-list', render: renderFileList },
    { url: '/api/all-video-files/', containerId: 'all-video-files-list', render: renderFileList },
    { url: '/api/all-image-files/', containerId: 'all-image-files-list', render: renderFileList },

    // Content endpoints (except news/events which are merged)
    { url: '/api/latest-news-events/', containerId: 'latest-news-events-list', render: renderContentList },
    // Use our custom render for department contents
    { url: '/api/department-contents/', containerId: 'department-contents-list', render: renderDepartmentComponents },
    { url: '/api/top-blogs-contents/', containerId: 'top-blogs-contents-list', render: renderContentList },
    { url: '/api/top-projects-contents/', containerId: 'top-projects-contents-list', render: renderContentList },
    { url: '/api/all-news-contents/', containerId: 'all-news-contents-list', render: renderContentList },
    { url: '/api/all-events-contents/', containerId: 'all-events-contents-list', render: renderContentList },
    { url: '/api/all-blogs-contents/', containerId: 'all-blogs-contents-list', render: renderContentList },
    { url: '/api/all-projects-contents/', containerId: 'all-projects-contents-list', render: renderContentList }
  ];

  // Loop through each endpoint and fetch its data.
  endpoints.forEach(endpoint => {
    fetchAndRender(endpoint.url, endpoint.containerId, endpoint.render);
  });

  // Fetch and render the merged news/events carousel.
  fetchAndRenderNewsEvents();
});
