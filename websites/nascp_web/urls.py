# nascp_web/urls.py
from django import views
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
import nascp_web.views as views

# from websites import nascp_web


def spa_view(request):
    return render(request, "index.html")


urlpatterns = [
    # Core prefixes
    path("admin/",   admin.site.urls),
    path("vision-mission-and-mandate/", views.vision_mission_mandate, name="vision_mission_mandate"),
    path("nascp-brief/", views.nascp_brief, name="nascp_brief"),
    # path("summernote/", include("django_summernote.urls")),  # ← REQUIRED
    path("ckeditor/", include("ckeditor_uploader.urls")),  # if using uploader
    path("", include("apps.content_creator.urls", namespace="content_creator")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("api/",     include("apps.api.urls")),
    path("audit/",   include("apps.audit.urls")),
    # path("summernote/", include("django_summernote.urls")),
    # Catch-all for the SPA — keep this LAST 
    re_path(r"^.*$", spa_view, name="spa"),
]

# Static & media in DEBUG nascep_brief.html
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
