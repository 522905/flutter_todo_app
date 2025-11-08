"""
Email notification service.
"""
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class EmailService:
    """Service for sending email notifications"""

    @staticmethod
    def send_task_reminder(user, task):
        """Send task reminder email"""
        try:
            subject = f"Reminder: {task.title}"
            message = f"""
            Hello {user.get_full_name()},

            This is a reminder for your task:

            Task: {task.title}
            Description: {task.description or 'No description'}
            Priority: {task.get_priority_display()}
            Due Date: {task.due_date.strftime('%Y-%m-%d %H:%M') if task.due_date else 'Not set'}

            Don't forget to complete it!

            Best regards,
            Todo App Team
            """

            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )

            logger.info(f"Task reminder email sent to {user.email} for task {task.id}")
            return True

        except Exception as e:
            logger.error(f"Failed to send email to {user.email}: {str(e)}")
            return False

    @staticmethod
    def send_daily_summary(user, tasks):
        """Send daily summary of pending tasks"""
        try:
            subject = f"Daily Task Summary - {len(tasks)} pending tasks"

            task_list = "\n".join([
                f"- {task.title} (Priority: {task.get_priority_display()})"
                for task in tasks
            ])

            message = f"""
            Hello {user.get_full_name()},

            You have {len(tasks)} pending tasks for today:

            {task_list}

            Keep up the good work!

            Best regards,
            Todo App Team
            """

            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )

            logger.info(f"Daily summary email sent to {user.email}")
            return True

        except Exception as e:
            logger.error(f"Failed to send daily summary to {user.email}: {str(e)}")
            return False
