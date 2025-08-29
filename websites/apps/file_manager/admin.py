from django.contrib import admin
from django.utils.html import format_html
from .models import File

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    # Display key fields in the admin list view
    list_display = ('title', 'file_type', 'category', 'uploaded_by', 'created_at', 'updated_at', 'preview')
    # Allow filtering by file type, category, and creation date
    list_filter = ('file_type', 'category', 'created_at')
    # Enable searching by title, description, and category
    search_fields = ('title', 'description', 'category')
    # Order by most recent uploads first
    ordering = ('-created_at',)
    # Make certain fields read-only in the admin
    readonly_fields = ('created_at', 'updated_at', 'preview')

    def preview(self, obj):
        """
        Returns a small thumbnail image if the file is of type 'image'.
        For other file types, display a simple message.
        """
        if obj.file_type == 'image' and obj.file:
            return format_html('<img src="{}" style="max-height: 50px;" />', obj.file.url)
        return "No preview"

    preview.short_description = "Preview"
