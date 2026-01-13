from http import HTTPStatus
from apps.hostel.models import RoomType
from apps.hostel.serializers import RoomTypeSerializer
from utils.base_result import BaseResultWithData


class RoomTypeQuery:
    
    @staticmethod
    def GetAll():
        try:
            room_types = RoomType.objects.all()
            serializer = RoomTypeSerializer(room_types, many=True)
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
            room_type = RoomType.objects.get(id=room_type_id)
            serializer = RoomTypeSerializer(room_type)
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
