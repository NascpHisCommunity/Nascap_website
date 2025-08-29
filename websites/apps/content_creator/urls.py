from django.urls import path
from .views import (
    ContentListView, ContentDetailView, ContentCreateView,
    ContentUpdateView, ContentDeleteView, CategoryListView,
    CategoryDetailView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView,
)

app_name = 'content_creator'

urlpatterns = [
    # Content URLs
    path('contents/', ContentListView.as_view(), name='content_list'),
    path('contents/create/', ContentCreateView.as_view(), name='content_create'),
    path('contents/<slug:slug>/', ContentDetailView.as_view(), name='content_detail'),
    path('contents/<slug:slug>/update/', ContentUpdateView.as_view(), name='content_update'),
    path('contents/<slug:slug>/delete/', ContentDeleteView.as_view(), name='content_delete'),

    # Category URLs
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/create/', CategoryCreateView.as_view(), name='category_create'),
    path('categories/<slug:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('categories/<slug:slug>/update/', CategoryUpdateView.as_view(), name='category_update'),
    path('categories/<slug:slug>/delete/', CategoryDeleteView.as_view(), name='category_delete'),
]
