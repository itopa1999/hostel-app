from http import HTTPStatus
from apps.hostel.models import Booking
from apps.hostel.serializers import BookingSerializer
from utils.base_result import BaseResultWithData
from utils.cache_helper import GlobalCache
from utils.enums import CacheKeys


class BookingQuery:
    
    @staticmethod
    def GetAll():
        try:
            # Try cache first
            cached_data = GlobalCache.get(CacheKeys.BOOKING_ALL.value)
            if cached_data:
                return BaseResultWithData(
                    data=cached_data,
                    status_code=HTTPStatus.OK,
                    message="Bookings retrieved successfully (cached)"
                )
            
            bookings = Booking.objects.all()
            serializer = BookingSerializer(bookings, many=True)
            
            # Cache the result
            GlobalCache.set(CacheKeys.BOOKING_ALL.value, serializer.data)
            
            return BaseResultWithData(
                data=serializer.data,
                status_code=HTTPStatus.OK,
                message="Bookings retrieved successfully"
            )
        except Exception as e:
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.BAD_REQUEST,
                message=str(e)
            )
    
    @staticmethod
    def GetById(booking_id):
        try:
            # Try cache first
            cache_key = CacheKeys.format(CacheKeys.BOOKING_ID, booking_id=booking_id)
            cached_data = GlobalCache.get(cache_key)
            if cached_data:
                return BaseResultWithData(
                    data=cached_data,
                    status_code=HTTPStatus.OK,
                    message="Booking retrieved successfully (cached)"
                )
            
            booking = Booking.objects.get(id=booking_id)
            serializer = BookingSerializer(booking)
            
            # Cache the result
            GlobalCache.set(cache_key, serializer.data)
            
            return BaseResultWithData(
                data=serializer.data,
                status_code=HTTPStatus.OK,
                message="Booking retrieved successfully"
            )
        except Booking.DoesNotExist:
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.NOT_FOUND,
                message="Booking not found"
            )
        except Exception as e:
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.BAD_REQUEST,
                message=str(e)
            )
