"""
Celery configuration for todo_backend project.
"""
import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('todo_backend')

# Load config from Django settings with CELERY namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from all registered Django apps
app.autodiscover_tasks()

# Celery Beat schedule for periodic tasks
app.conf.beat_schedule = {
    # Check for due task reminders every minute
    'check-task-reminders': {
        'task': 'notifications.tasks.check_and_send_reminders',
        'schedule': crontab(minute='*/1'),  # Every minute
    },
    # Send daily summary emails at 8 AM
    'send-daily-summaries': {
        'task': 'notifications.tasks.send_daily_summaries',
        'schedule': crontab(hour=8, minute=0),  # 8:00 AM daily
    },
    # Clean up old notifications weekly
    'cleanup-old-notifications': {
        'task': 'notifications.tasks.cleanup_old_notifications',
        'schedule': crontab(hour=2, minute=0, day_of_week=1),  # Monday 2 AM
    },
}

@app.task(bind=True)
def debug_task(self):
    """Debug task for testing Celery"""
    print(f'Request: {self.request!r}')
