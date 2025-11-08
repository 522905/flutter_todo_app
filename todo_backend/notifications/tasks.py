"""
Celery tasks for notifications.
"""
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .services.email_service import EmailService
from .services.whatsapp_service import WhatsAppService
from .services.push_service import PushNotificationService
from .models import Notification
import logging

logger = logging.getLogger(__name__)


@shared_task
def check_and_send_reminders():
    """Check for tasks with upcoming reminders and send notifications"""
    from tasks.models import Task
    from django.contrib.auth import get_user_model

    User = get_user_model()

    now = timezone.now()
    upcoming_time = now + timedelta(minutes=5)

    # Find tasks with reminders in the next 5 minutes
    tasks_to_remind = Task.objects.filter(
        reminder_time__gte=now,
        reminder_time__lte=upcoming_time,
        is_completed=False,
        deleted_at__isnull=True
    ).select_related('user')

    for task in tasks_to_remind:
        user = task.user

        # Email notification
        if user.email_notifications:
            send_email_notification.delay(user.id, task.id)

        # WhatsApp notification
        if user.whatsapp_notifications and user.phone_number:
            send_whatsapp_notification.delay(user.id, task.id)

        # Push notification
        if user.push_notifications and user.fcm_token:
            send_push_notification.delay(user.id, task.id)

    logger.info(f"Checked reminders: {tasks_to_remind.count()} tasks found")
    return tasks_to_remind.count()


@shared_task
def send_email_notification(user_id, task_id):
    """Send email notification for a task"""
    from tasks.models import Task
    from django.contrib.auth import get_user_model

    User = get_user_model()

    try:
        user = User.objects.get(id=user_id)
        task = Task.objects.get(id=task_id)

        success = EmailService.send_task_reminder(user, task)

        # Log notification
        Notification.objects.create(
            user=user,
            task=task,
            type='EMAIL',
            status='SENT' if success else 'FAILED',
            message=f"Reminder for task: {task.title}",
            subject=f"Reminder: {task.title}",
            scheduled_at=timezone.now()
        )

        return success

    except Exception as e:
        logger.error(f"Email notification failed: {str(e)}")
        return False


@shared_task
def send_whatsapp_notification(user_id, task_id):
    """Send WhatsApp notification for a task"""
    from tasks.models import Task
    from django.contrib.auth import get_user_model

    User = get_user_model()

    try:
        user = User.objects.get(id=user_id)
        task = Task.objects.get(id=task_id)

        success = WhatsAppService.send_task_reminder(user, task)

        # Log notification
        Notification.objects.create(
            user=user,
            task=task,
            type='WHATSAPP',
            status='SENT' if success else 'FAILED',
            message=f"WhatsApp reminder for: {task.title}",
            scheduled_at=timezone.now()
        )

        return success

    except Exception as e:
        logger.error(f"WhatsApp notification failed: {str(e)}")
        return False


@shared_task
def send_push_notification(user_id, task_id):
    """Send push notification for a task"""
    from tasks.models import Task
    from django.contrib.auth import get_user_model

    User = get_user_model()

    try:
        user = User.objects.get(id=user_id)
        task = Task.objects.get(id=task_id)

        success = PushNotificationService.send_task_reminder(user, task)

        # Log notification
        Notification.objects.create(
            user=user,
            task=task,
            type='PUSH',
            status='SENT' if success else 'FAILED',
            message=f"Push reminder for: {task.title}",
            scheduled_at=timezone.now()
        )

        return success

    except Exception as e:
        logger.error(f"Push notification failed: {str(e)}")
        return False


@shared_task
def send_daily_summaries():
    """Send daily task summaries to all users"""
    from tasks.models import Task
    from django.contrib.auth import get_user_model

    User = get_user_model()

    users = User.objects.filter(email_notifications=True)

    for user in users:
        pending_tasks = Task.objects.filter(
            user=user,
            is_completed=False,
            deleted_at__isnull=True
        )[:10]  # Limit to 10 tasks

        if pending_tasks.exists():
            EmailService.send_daily_summary(user, pending_tasks)

    logger.info(f"Daily summaries sent to {users.count()} users")
    return users.count()


@shared_task
def cleanup_old_notifications():
    """Clean up old notifications (older than 30 days)"""
    cutoff_date = timezone.now() - timedelta(days=30)
    deleted_count = Notification.objects.filter(created_at__lt=cutoff_date).delete()[0]

    logger.info(f"Cleaned up {deleted_count} old notifications")
    return deleted_count
