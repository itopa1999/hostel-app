from apps.hostel.models import Room
from utils.base_result import BaseResultWithData


class RoomQuery:
    
    @staticmethod
    def GetAll():
        try:
            rooms = Room.objects.filter(is_deleted=False)
            return BaseResultWithData(True, "Rooms retrieved successfully", list(rooms), 200)
        except Exception as e:
            return BaseResultWithData(False, str(e), None, 400)
    
    @staticmethod
    def GetById(room_id):
        try:
            room = Room.objects.get(id=room_id, is_deleted=False)
            return BaseResultWithData(True, "Room retrieved successfully", room, 200)
        except Room.DoesNotExist:
            return BaseResultWithData(False, "Room not found", None, 404)
        except Exception as e:
            return BaseResultWithData(False, str(e), None, 400)
