from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class Category(models.Model):
    """
    Represents a content category used to group and filter
    content items (e.g., news, events, blogs).
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("content_creator:category_detail", kwargs={"slug": self.slug})


class Content(models.Model):
    """
    Stores write-ups such as department details, news, announcements,
    events, or blog posts. Each item can be linked to a category.
    """
    CONTENT_TYPE_CHOICES = (
        ("department", "Department Details"),
        ("news", "News"),
        ("announcement", "Announcement"),
        ("event", "Event"),
        ("blog", "Blog"),
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="contents",
    )
    # Plain TextField; Summernote provides the rich editor at the form/admin layer
    body = models.TextField()
    published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at", "-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("content_creator:content_detail", kwargs={"slug": self.slug})
