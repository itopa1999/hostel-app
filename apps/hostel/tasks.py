from celery import shared_task
from apps.hostel.models import Booking, Hotel
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def generate_booking_report(self, booking_id):
    """
    Generate booking report asynchronously
    Retries 3 times on failure
    """
    try:
        booking = Booking.objects.get(id=booking_id)
        # Generate report logic here
        logger.info(f"Booking report generated for booking {booking_id}")
        return f"Report generated for booking {booking_id}"
    except Booking.DoesNotExist:
        logger.error(f"Booking {booking_id} not found")
        return "Booking not found"
    except Exception as exc:
        logger.error(f"Failed to generate booking report: {exc}")
        raise self.retry(exc=exc, countdown=60)


@shared_task(bind=True, max_retries=3)
def send_booking_confirmation(self, booking_id):
    """
    Send booking confirmation email
    Retries 3 times on failure
    """
    try:
        booking = Booking.objects.get(id=booking_id)
        # Send confirmation email logic here
        logger.info(f"Booking confirmation sent for booking {booking_id}")
        return f"Confirmation sent for booking {booking_id}"
    except Booking.DoesNotExist:
        logger.error(f"Booking {booking_id} not found")
        return "Booking not found"
    except Exception as exc:
        logger.error(f"Failed to send booking confirmation: {exc}")
        raise self.retry(exc=exc, countdown=60)


@shared_task(bind=True, max_retries=3)
def cleanup_expired_bookings(self):
    """
    Clean up expired bookings
    Retries 3 times on failure
    """
    try:
        from datetime import datetime, timedelta
        expired_date = datetime.now() - timedelta(days=30)
        # Cleanup logic here
        logger.info("Expired bookings cleanup completed")
        return "Cleanup completed"
    except Exception as exc:
        logger.error(f"Failed to cleanup bookings: {exc}")
        raise self.retry(exc=exc, countdown=120)
