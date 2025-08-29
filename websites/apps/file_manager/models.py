from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class File(models.Model):
    # Define the type choices for uploaded files.
    FILE_TYPE_CHOICES = (
        ('document', 'Document'),
        ('image', 'Image'),
        ('video', 'Video'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    # The FileField will store the uploaded file and organize uploads by date.
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')
    # You can use a CharField for category or later replace it with a ForeignKey to a Category model.
    category = models.CharField(max_length=100, blank=True, null=True)
    file_type = models.CharField(max_length=20, choices=FILE_TYPE_CHOICES)
    # Optional: Record the user (e.g., admin) who uploaded the file.
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='uploaded_files'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Order files by the most recent uploads first.
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """
        Return the URL to view file details. Make sure you have a corresponding URL pattern named 'file_detail'.
        """
        from django.urls import reverse
        return reverse('file_manager:file_detail', kwargs={'pk': self.pk})

    @property
    def extension(self):
        """
        Utility property to get the file extension.
        """
        import os
        return os.path.splitext(self.file.name)[1].lower()
