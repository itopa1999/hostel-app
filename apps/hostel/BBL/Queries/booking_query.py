from http import HTTPStatus
from apps.hostel.models import Booking
from apps.hostel.serializers import BookingSerializer
from utils.base_result import BaseResultWithData


class BookingQuery:
    
    @staticmethod
    def GetAll():
        try:
            bookings = Booking.objects.all()
            serializer = BookingSerializer(bookings, many=True)
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
            booking = Booking.objects.get(id=booking_id)
            serializer = BookingSerializer(booking)
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
