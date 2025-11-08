"""
User models for the application.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class User(AbstractUser):
    """Extended User model with additional fields"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, db_index=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    # Notification preferences
    fcm_token = models.CharField(max_length=255, blank=True, null=True, help_text="Firebase Cloud Messaging token")
    email_notifications = models.BooleanField(default=True, help_text="Enable email notifications")
    whatsapp_notifications = models.BooleanField(default=False, help_text="Enable WhatsApp notifications")
    push_notifications = models.BooleanField(default=True, help_text="Enable push notifications")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Make email the username field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.email} ({self.get_full_name()})"

    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in between."""
        full_name = f'{self.first_name} {self.last_name}'.strip()
        return full_name or self.username
