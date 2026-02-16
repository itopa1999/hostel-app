from http import HTTPStatus
from apps.hostel.models import GuestProfile
from apps.hostel.serializers import GuestProfileSerializer
from utils.base_result import BaseResultWithData
from utils.cache_helper import GlobalCache
from utils.enums import CacheKeys


class GuestProfileQuery:
    
    @staticmethod
    def GetAll():
        try:
            # Try cache first
            cached_data = GlobalCache.get(CacheKeys.GUEST_ALL.value)
            if cached_data:
                return BaseResultWithData(
                    data=cached_data,
                    status_code=HTTPStatus.OK,
                    message="Guest profiles retrieved successfully (cached)"
                )
            
            guests = GuestProfile.objects.all()
            serializer = GuestProfileSerializer(guests, many=True)
            
            # Cache the result
            GlobalCache.set(CacheKeys.GUEST_ALL.value, serializer.data)
            
            return BaseResultWithData(
                data=serializer.data,
                status_code=HTTPStatus.OK,
                message="Guest profiles retrieved successfully"
            )
        except Exception as e:
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.BAD_REQUEST,
                message=str(e)
            )
    
    @staticmethod
    def GetById(guest_id):
        try:
            # Try cache first
            cache_key = CacheKeys.format(CacheKeys.GUEST_ID, guest_id=guest_id)
            cached_data = GlobalCache.get(cache_key)
            if cached_data:
                return BaseResultWithData(
                    data=cached_data,
                    status_code=HTTPStatus.OK,
                    message="Guest profile retrieved successfully (cached)"
                )
            
            guest = GuestProfile.objects.get(id=guest_id)
            serializer = GuestProfileSerializer(guest)
            
            # Cache the result
            GlobalCache.set(cache_key, serializer.data)
            
            return BaseResultWithData(
                data=serializer.data,
                status_code=HTTPStatus.OK,
                message="Guest profile retrieved successfully"
            )
        except GuestProfile.DoesNotExist:
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.NOT_FOUND,
                message="Guest profile not found"
            )
        except Exception as e:
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.BAD_REQUEST,
                message=str(e)
            )
