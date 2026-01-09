from http import HTTPStatus
from django.db.models import Count, Sum, Q
from apps.hostel.models import Hotel, Floor, Room, RoomType, GuestProfile, Booking, Invoice, Payment
from utils.enums import RoomStatus, BookingStatus, PaymentStatus
from utils.base_result import BaseResultWithData
import logging

logger = logging.getLogger(__name__)


class DashboardQuery:
    """Handle admin dashboard data retrieval"""
    
    @staticmethod
    def GetDashboardMetrics():
        """
        Retrieve comprehensive dashboard metrics for admin panel.
        
        Returns:
            BaseResultWithData: Result with dashboard statistics
        """
        # Count statistics
        total_hotels = Hotel.objects.filter(is_deleted=False).count()
        total_floors = Floor.objects.filter(is_deleted=False).count()
        total_rooms = Room.objects.filter(is_deleted=False).count()
        total_guests = GuestProfile.objects.filter(is_deleted=False).count()
        total_bookings = Booking.objects.filter(is_deleted=False).count()
        total_invoices = Invoice.objects.filter(is_deleted=False).count()
        total_payments = Payment.objects.filter(is_deleted=False).count()
        
        # Room status breakdown
        room_available = Room.objects.filter(
            is_deleted=False,
            status=RoomStatus.AVAILABLE.value
        ).count()
        room_occupied = Room.objects.filter(
            is_deleted=False,
            status=RoomStatus.OCCUPIED.value
        ).count()
        room_dirty = Room.objects.filter(
            is_deleted=False,
            status=RoomStatus.DIRTY.value
        ).count()
        room_maintenance = Room.objects.filter(
            is_deleted=False,
            status=RoomStatus.MAINTENANCE.value
        ).count()
        
        # Booking status breakdown
        booking_reserved = Booking.objects.filter(
            is_deleted=False,
            status=BookingStatus.RESERVED.value
        ).count()
        booking_checked_in = Booking.objects.filter(
            is_deleted=False,
            status=BookingStatus.CHECKED_IN.value
        ).count()
        booking_checked_out = Booking.objects.filter(
            is_deleted=False,
            status=BookingStatus.CHECKED_OUT.value
        ).count()
        booking_cancelled = Booking.objects.filter(
            is_deleted=False,
            status=BookingStatus.CANCELLED.value
        ).count()
        
        # Payment status breakdown
        payment_pending = Payment.objects.filter(
            is_deleted=False,
            payment_status=PaymentStatus.PENDING.value
        ).count()
        payment_completed = Payment.objects.filter(
            is_deleted=False,
            payment_status=PaymentStatus.COMPLETED.value
        ).count()
        payment_failed = Payment.objects.filter(
            is_deleted=False,
            payment_status=PaymentStatus.FAILED.value
        ).count()
        payment_refunded = Payment.objects.filter(
            is_deleted=False,
            payment_status=PaymentStatus.REFUNDED.value
        ).count()
        
        # Financial metrics
        total_revenue = Payment.objects.filter(
            is_deleted=False,
            payment_status=PaymentStatus.COMPLETED.value
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        pending_payments = Payment.objects.filter(
            is_deleted=False,
            payment_status=PaymentStatus.PENDING.value
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # Recent bookings
        recent_bookings = list(
            Booking.objects.filter(is_deleted=False)
            .select_related('guest', 'room')
            .order_by('-created_at')[:5]
            .values(
                'id', 'confirmation_code', 'guest__name',
                'check_in', 'check_out', 'status', 'created_at'
            )
        )
        
        # Recent payments
        recent_payments = list(
            Payment.objects.filter(is_deleted=False)
            .select_related('invoice')
            .order_by('-created_at')[:5]
            .values(
                'id', 'amount', 'method', 'payment_status',
                'invoice__invoice_number', 'created_at'
            )
        )
        
        # Hotel occupancy
        hotels_data = []
        for hotel in Hotel.objects.filter(is_deleted=False):
            total_rooms_hotel = hotel.rooms.filter(is_deleted=False).count()
            occupied_rooms = hotel.rooms.filter(
                is_deleted=False,
                status=RoomStatus.OCCUPIED.value
            ).count()
            occupancy_rate = (occupied_rooms / total_rooms_hotel * 100) if total_rooms_hotel > 0 else 0
            
            hotels_data.append({
                'id': hotel.id,
                'name': hotel.name,
                'total_rooms': total_rooms_hotel,
                'occupied_rooms': occupied_rooms,
                'available_rooms': hotel.rooms.filter(
                    is_deleted=False,
                    status=RoomStatus.AVAILABLE.value
                ).count(),
                'occupancy_rate': round(occupancy_rate, 2),
            })
        
        result_data = {
            'summary': {
                'total_hotels': total_hotels,
                'total_floors': total_floors,
                'total_rooms': total_rooms,
                'total_guests': total_guests,
                'total_bookings': total_bookings,
                'total_invoices': total_invoices,
                'total_payments': total_payments,
            },
            'room_status': {
                'available': room_available,
                'occupied': room_occupied,
                'dirty': room_dirty,
                'maintenance': room_maintenance,
            },
            'booking_status': {
                'reserved': booking_reserved,
                'checked_in': booking_checked_in,
                'checked_out': booking_checked_out,
                'cancelled': booking_cancelled,
            },
            'payment_status': {
                'pending': payment_pending,
                'completed': payment_completed,
                'failed': payment_failed,
                'refunded': payment_refunded,
            },
            'financial': {
                'total_revenue': float(total_revenue),
                'pending_payments': float(pending_payments),
            },
            'recent_bookings': recent_bookings,
            'recent_payments': recent_payments,
            'hotels': hotels_data,
        }
        
        return BaseResultWithData(
            message="Dashboard metrics retrieved successfully",
            data=result_data,
            status_code=HTTPStatus.OK
        )
