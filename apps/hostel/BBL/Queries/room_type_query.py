from http import HTTPStatus
from apps.hostel.models import RoomType
from apps.hostel.serializers import RoomTypeSerializer
from utils.base_result import BaseResultWithData
from utils.cache_helper import GlobalCache
from utils.enums import CacheKeys


class RoomTypeQuery:
    
    @staticmethod
    def GetAll():
        try:
            # Try cache first
            cached_data = GlobalCache.get(CacheKeys.ROOM_TYPE_ALL.value)
            if cached_data:
                return BaseResultWithData(
                    data=cached_data,
                    status_code=HTTPStatus.OK,
                    message="Room types retrieved successfully (cached)"
                )
            
            room_types = RoomType.objects.all()
            serializer = RoomTypeSerializer(room_types, many=True)
            
            # Cache the result
            GlobalCache.set(CacheKeys.ROOM_TYPE_ALL.value, serializer.data)
            
            return BaseResultWithData(
                data=serializer.data,
                status_code=HTTPStatus.OK,
                message="Room types retrieved successfully"
            )
        except Exception as e:
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.BAD_REQUEST,
                message=str(e)
            )
    
    @staticmethod
    def GetById(room_type_id):
        try:
            # Try cache first
            cache_key = CacheKeys.format(CacheKeys.ROOM_TYPE_ID, room_type_id=room_type_id)
            cached_data = GlobalCache.get(cache_key)
            if cached_data:
                return BaseResultWithData(
                    data=cached_data,
                    status_code=HTTPStatus.OK,
                    message="Room type retrieved successfully (cached)"
                )
            
            room_type = RoomType.objects.get(id=room_type_id)
            serializer = RoomTypeSerializer(room_type)
            
            # Cache the result
            GlobalCache.set(cache_key, serializer.data)
            
            return BaseResultWithData(
                data=serializer.data,
                status_code=HTTPStatus.OK,
                message="Room type retrieved successfully"
            )
        except RoomType.DoesNotExist:
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.NOT_FOUND,
                message="Room type not found"
            )
        except Exception as e:
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.BAD_REQUEST,
                message=str(e)
            )
