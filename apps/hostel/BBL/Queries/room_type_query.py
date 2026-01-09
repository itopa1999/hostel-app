from apps.hostel.models import RoomType
from utils.base_result import BaseResultWithData


class RoomTypeQuery:
    
    @staticmethod
    def GetAll():
        try:
            room_types = RoomType.objects.filter(is_deleted=False)
            return BaseResultWithData(True, "Room types retrieved successfully", list(room_types), 200)
        except Exception as e:
            return BaseResultWithData(False, str(e), None, 400)
    
    @staticmethod
    def GetById(room_type_id):
        try:
            room_type = RoomType.objects.get(id=room_type_id, is_deleted=False)
            return BaseResultWithData(True, "Room type retrieved successfully", room_type, 200)
        except RoomType.DoesNotExist:
            return BaseResultWithData(False, "Room type not found", None, 404)
        except Exception as e:
            return BaseResultWithData(False, str(e), None, 400)
