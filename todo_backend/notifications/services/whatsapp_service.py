"""
WhatsApp notification service using Twilio.
"""
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class WhatsAppService:
    """Service for sending WhatsApp notifications via Twilio"""

    @staticmethod
    def send_task_reminder(user, task):
        """Send task reminder via WhatsApp"""
        if not user.phone_number:
            logger.warning(f"User {user.email} has no phone number")
            return False

        if not settings.TWILIO_ACCOUNT_SID or not settings.TWILIO_AUTH_TOKEN:
            logger.warning("Twilio credentials not configured")
            return False

        try:
            from twilio.rest import Client

            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

            message_body = f"""
🔔 Task Reminder!

*{task.title}*

Priority: {task.get_priority_display()}
Due: {task.due_date.strftime('%Y-%m-%d %H:%M') if task.due_date else 'Not set'}

{task.description[:100] if task.description else ''}

Don't forget to complete it!
            """.strip()

            message = client.messages.create(
                from_=settings.TWILIO_WHATSAPP_FROM,
                body=message_body,
                to=f'whatsapp:{user.phone_number}'
            )

            logger.info(f"WhatsApp reminder sent to {user.phone_number} - SID: {message.sid}")
            return True

        except Exception as e:
            logger.error(f"Failed to send WhatsApp to {user.phone_number}: {str(e)}")
            return False

    @staticmethod
    def send_urgent_notification(user, message_text):
        """Send urgent WhatsApp notification"""
        if not user.phone_number:
            return False

        if not settings.TWILIO_ACCOUNT_SID or not settings.TWILIO_AUTH_TOKEN:
            return False

        try:
            from twilio.rest import Client

            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

            message = client.messages.create(
                from_=settings.TWILIO_WHATSAPP_FROM,
                body=f"🚨 Urgent: {message_text}",
                to=f'whatsapp:{user.phone_number}'
            )

            logger.info(f"Urgent WhatsApp sent to {user.phone_number} - SID: {message.sid}")
            return True

        except Exception as e:
            logger.error(f"Failed to send urgent WhatsApp: {str(e)}")
            return False
