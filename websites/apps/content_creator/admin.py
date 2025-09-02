from django.contrib import admin
from .models import Category, Content
from .forms import ContentForm, CategoryForm

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    form = CategoryForm
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)

@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    form = ContentForm
    list_display  = ("title", "content_type", "category", "published", "published_at", "created_at")
    list_filter   = ("content_type", "published", "category")
    search_fields = ("title", "body")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"
