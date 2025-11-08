"""
Notification models for the application.
"""
from django.db import models
from django.conf import settings
import uuid


class Notification(models.Model):
    """Notification model for tracking sent notifications"""

    TYPE_CHOICES = [
        ('EMAIL', 'Email'),
        ('WHATSAPP', 'WhatsApp'),
        ('PUSH', 'Push Notification'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SENT', 'Sent'),
        ('FAILED', 'Failed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    task = models.ForeignKey('tasks.Task', on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)

    # Notification details
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    message = models.TextField()
    subject = models.CharField(max_length=255, blank=True, null=True)

    # Metadata
    error_message = models.TextField(blank=True, null=True)
    retry_count = models.IntegerField(default=0)

    # Timestamps
    scheduled_at = models.DateTimeField()
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'notifications'
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['type', 'status']),
            models.Index(fields=['scheduled_at']),
        ]

    def __str__(self):
        return f"{self.type} notification for {self.user.email} - {self.status}"

    def mark_sent(self):
        """Mark notification as sent"""
        from django.utils import timezone
        self.status = 'SENT'
        self.sent_at = timezone.now()
        self.save()

    def mark_failed(self, error_msg):
        """Mark notification as failed"""
        self.status = 'FAILED'
        self.error_message = error_msg
        self.retry_count += 1
        self.save()
