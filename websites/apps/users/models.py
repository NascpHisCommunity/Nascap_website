from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """
    Custom user model that extends the default Django AbstractUser.
    This model adds a role field and optional profile information.
    """
    
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('editor', 'Editor'),
        ('viewer', 'Viewer'),
    )
    
    # Role to manage different types of admin users and their permissions.
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='viewer',
        help_text="Designates the user's role which determines permissions."
    )
    
    # Optional: Additional profile information
    bio = models.TextField(
        blank=True,
        null=True,
        help_text="A short biography of the user."
    )
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True,
        help_text="Optional profile image for the user."
    )
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
