from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin   # ← add
from .models import Category, Content
from .forms  import ContentForm, CategoryForm              # ← optional but tidy

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    form = CategoryForm                    # ← so description textarea rows/placeholder show
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Content)
class ContentAdmin(SummernoteModelAdmin):  # ← inherits Summernote’s media
    form = ContentForm                     # ← forces the SummernoteWidget
    summernote_fields = ("body",)          # ← not strictly required but nice & explicit

    list_display  = ("title", "content_type", "category",
                     "published", "published_at", "created_at")
    list_filter   = ("content_type", "published", "category")
    search_fields = ("title", "body")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"
