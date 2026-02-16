from http import HTTPStatus
from apps.hostel.models import Room
from apps.hostel.serializers import RoomSerializer
from utils.base_result import BaseResultWithData
from utils.cache_helper import GlobalCache
from utils.enums import CacheKeys


class RoomQuery:
    
    @staticmethod
    def GetAll():
        try:
            # Try cache first
            cached_data = GlobalCache.get(CacheKeys.ROOM_ALL.value)
            if cached_data:
                return BaseResultWithData(
                    data=cached_data,
                    status_code=HTTPStatus.OK,
                    message="Rooms retrieved successfully (cached)"
                )
            
            rooms = Room.objects.all()
            serializer = RoomSerializer(rooms, many=True)
            
            # Cache the result
            GlobalCache.set(CacheKeys.ROOM_ALL.value, serializer.data)
            
            return BaseResultWithData(
                data=serializer.data,
                status_code=HTTPStatus.OK,
                message="Rooms retrieved successfully"
            )
        except Exception as e:
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.BAD_REQUEST,
                message=str(e)
            )
    
    @staticmethod
    def GetById(room_id):
        try:
            # Try cache first
            cache_key = CacheKeys.format(CacheKeys.ROOM_ID, room_id=room_id)
            cached_data = GlobalCache.get(cache_key)
            if cached_data:
                return BaseResultWithData(
                    data=cached_data,
                    status_code=HTTPStatus.OK,
                    message="Room retrieved successfully (cached)"
                )
            
            room = Room.objects.get(id=room_id)
            serializer = RoomSerializer(room)
            
            # Cache the result
            GlobalCache.set(cache_key, serializer.data)
            
            return BaseResultWithData(
                data=serializer.data,
                status_code=HTTPStatus.OK,
                message="Room retrieved successfully"
            )
        except Room.DoesNotExist:
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.NOT_FOUND,
                message="Room not found"
            )
        except Exception as e:
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.BAD_REQUEST,
                message=str(e)
            )
