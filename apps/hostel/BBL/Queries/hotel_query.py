from http import HTTPStatus
from apps.hostel.models import Hotel
from apps.hostel.serializers import HotelSerializer
from utils.base_result import BaseResultWithData


class HotelQuery:
    
    @staticmethod
    def GetFirst():
        try:
            hotel = Hotel.objects.all().first()
            if not hotel:
                return BaseResultWithData(
                    data=None,
                    status_code=HTTPStatus.NOT_FOUND,
                    message="Hotel not found"
                )
            serializer = HotelSerializer(hotel)
            return BaseResultWithData(
                data=serializer.data,
                status_code=HTTPStatus.OK,
                message="Hotel retrieved successfully"
            )
        except Exception as e:
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.BAD_REQUEST,
                message=str(e)
            )
