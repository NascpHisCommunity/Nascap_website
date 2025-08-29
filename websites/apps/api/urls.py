# apps/api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.file_manager.api_views import FileViewSet
from .views import FileListAPIView
from . import views

router = DefaultRouter()
router.register(r'files', FileViewSet, basename='file')

urlpatterns = [
    path('', include(router.urls)),
    path('files/', FileListAPIView, name='api_file_list'),
    path('latest-news-events/', views.latest_news_events, name='latest_news_events'),
    path('department-contents/', views.department_contents, name='department_contents'),
    path('top-reports-files/', views.top_reports_files, name='top_reports_files'),
    path('top-publications-files/', views.top_publications_files, name='top_publications_files'),
    path('top-resources-files/', views.top_resources_files, name='top_resources_files'),
    path('top-analysis-files/', views.top_analysis_files, name='top_analysis_files'),
    path('all-reports-files-by-slug/', views.all_reports_files_by_slug, name='all_reports_files_by_slug'),
    path('all-publications-files/', views.all_publications_files, name='all_publications_files'),
    path('all-resources-files/', views.all_resources_files, name='all_resources_files'),
    path('all-analysis-files/', views.all_analysis_files, name='all_analysis_files'),
    path('top-news-contents/', views.top_news_contents, name='top_news_contents'),
    path('top-events-contents/', views.top_events_contents, name='top_events_contents'),
    path('top-blogs-contents/', views.top_blogs_contents, name='top_blogs_contents'),
    path('top-projects-contents/', views.top_projects_contents, name='top_projects_contents'),
    path('all-news-contents/', views.all_news_contents, name='all_news_contents'),
    path('all-events-contents/', views.all_events_contents, name='all_events_contents'),
    path('all-blogs-contents/', views.all_blogs_contents, name='all_blogs_contents'),
    path('all-projects-contents/', views.all_projects_contents, name='all_projects_contents'),
    path('top-video-files/', views.top_video_files, name='top_video_files'),
    path('top-image-files/', views.top_image_files, name='top_image_files'),
    path('all-video-files/', views.all_video_files, name='all_video_files'),
    path('all-image-files/', views.all_image_files, name='all_image_files'),
]
