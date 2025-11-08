"""
Task models for the application.
"""
from django.db import models
from django.conf import settings
import uuid


class Task(models.Model):
    """Task model for managing user tasks"""

    CATEGORY_CHOICES = [
        ('WORK', 'Work'),
        ('PERSONAL', 'Personal'),
        ('SHOPPING', 'Shopping'),
        ('HEALTH', 'Health'),
        ('FINANCE', 'Finance'),
        ('EDUCATION', 'Education'),
        ('OTHER', 'Other'),
    ]

    PRIORITY_CHOICES = [
        ('HIGH', 'High'),
        ('MEDIUM', 'Medium'),
        ('LOW', 'Low'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks')

    # Task details
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='OTHER')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')

    # Status
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    # Dates
    due_date = models.DateTimeField(null=True, blank=True)
    reminder_time = models.DateTimeField(null=True, blank=True, help_text="When to send reminder")

    # Soft delete
    deleted_at = models.DateTimeField(null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tasks'
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_completed']),
            models.Index(fields=['user', 'category']),
            models.Index(fields=['due_date']),
            models.Index(fields=['reminder_time']),
        ]

    def __str__(self):
        return f"{self.title} ({self.user.email})"

    def mark_complete(self):
        """Mark task as completed"""
        from django.utils import timezone
        self.is_completed = True
        self.completed_at = timezone.now()
        self.save()

    def mark_incomplete(self):
        """Mark task as incomplete"""
        self.is_completed = False
        self.completed_at = None
        self.save()

    def soft_delete(self):
        """Soft delete the task"""
        from django.utils import timezone
        self.deleted_at = timezone.now()
        self.save()

    @property
    def is_overdue(self):
        """Check if task is overdue"""
        from django.utils import timezone
        if self.due_date and not self.is_completed:
            return timezone.now() > self.due_date
        return False
