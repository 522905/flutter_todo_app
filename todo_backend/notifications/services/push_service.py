"""
Push notification service using Firebase Cloud Messaging.
"""
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class PushNotificationService:
    """Service for sending push notifications via Firebase"""

    @staticmethod
    def send_task_reminder(user, task):
        """Send task reminder push notification"""
        if not user.fcm_token:
            logger.warning(f"User {user.email} has no FCM token")
            return False

        if not settings.FIREBASE_CREDENTIALS_PATH:
            logger.warning("Firebase credentials not configured")
            return False

        try:
            import firebase_admin
            from firebase_admin import credentials, messaging

            # Initialize Firebase (only once)
            if not firebase_admin._apps:
                cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
                firebase_admin.initialize_app(cred)

            message = messaging.Message(
                notification=messaging.Notification(
                    title=f"Reminder: {task.title}",
                    body=task.description[:100] if task.description else "Don't forget your task!",
                ),
                data={
                    'task_id': str(task.id),
                    'type': 'task_reminder',
                    'priority': task.priority,
                },
                token=user.fcm_token,
            )

            response = messaging.send(message)
            logger.info(f"Push notification sent to {user.email} - Response: {response}")
            return True

        except Exception as e:
            logger.error(f"Failed to send push notification to {user.email}: {str(e)}")
            return False

    @staticmethod
    def send_notification(user, title, body, data=None):
        """Send generic push notification"""
        if not user.fcm_token:
            return False

        if not settings.FIREBASE_CREDENTIALS_PATH:
            return False

        try:
            import firebase_admin
            from firebase_admin import credentials, messaging

            if not firebase_admin._apps:
                cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
                firebase_admin.initialize_app(cred)

            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body,
                ),
                data=data or {},
                token=user.fcm_token,
            )

            response = messaging.send(message)
            logger.info(f"Push notification sent - Response: {response}")
            return True

        except Exception as e:
            logger.error(f"Failed to send push notification: {str(e)}")
            return False
