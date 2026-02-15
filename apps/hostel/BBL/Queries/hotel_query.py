from http import HTTPStatus
from apps.hostel.models import Hotel
from apps.hostel.serializers import HotelSerializer
from utils.base_result import BaseResultWithData
from utils.cache_helper import GlobalCache
from utils.enums import CacheKeys


class HotelQuery:
    
    @staticmethod
    def GetFirst():
        try:
            # Try to get from cache first
            cached_hotel = GlobalCache.get(CacheKeys.HOTEL_FIRST.value)
            if cached_hotel:
                return BaseResultWithData(
                    data=cached_hotel,
                    status_code=HTTPStatus.OK,
                    message="Hotel retrieved successfully (cached)"
                )
            
            hotel = Hotel.objects.all().first()
            if not hotel:
                return BaseResultWithData(
                    data=None,
                    status_code=HTTPStatus.NOT_FOUND,
                    message="Hotel not found"
                )
            serializer = HotelSerializer(hotel)
            
            # Cache the result
            GlobalCache.set(CacheKeys.HOTEL_FIRST.value, serializer.data)
            
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
