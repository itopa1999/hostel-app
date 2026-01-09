from celery import shared_task
from django.core.mail import send_mail
from apps.users.models import User
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def send_user_notification_email(self, user_id, subject, message):
    """
    Send notification email to user
    Retries 3 times on failure
    """
    try:
        user = User.objects.get(id=user_id)
        send_mail(
            subject=subject,
            message=message,
            from_email='noreply@hostelapp.com',
            recipient_list=[user.email],
            fail_silently=False,
        )
        logger.info(f"Email sent successfully to user {user_id}")
        return f"Email sent to {user.email}"
    except User.DoesNotExist:
        logger.error(f"User {user_id} not found")
        return "User not found"
    except Exception as exc:
        logger.error(f"Failed to send email: {exc}")
        # Retry after 60 seconds, up to 3 times
        raise self.retry(exc=exc, countdown=60)


@shared_task(bind=True, max_retries=3)
def log_user_activity(self, user_id, action, details=None):
    """
    Log user activity asynchronously
    Retries 3 times on failure
    """
    try:
        user = User.objects.get(id=user_id)
        logger.info(f"User {user.username} performed action: {action} - Details: {details}")
        return f"Activity logged for user {user_id}"
    except Exception as exc:
        logger.error(f"Failed to log activity: {exc}")
        raise self.retry(exc=exc, countdown=30)
