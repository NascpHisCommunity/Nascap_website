# nascp_web/urls.py
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render


def spa_view(request):
    return render(request, "index.html")


urlpatterns = [
    # Core prefixes
    path("admin/",   admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("api/",     include("apps.api.urls")),
    path("audit/",   include("apps.audit.urls")),
    path("summernote/", include("django_summernote.urls")),
    # Catch-all for the SPA — keep this LAST
    re_path(r"^.*$", spa_view, name="spa"),
]

# Static & media in DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
