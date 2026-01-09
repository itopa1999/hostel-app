from apps.hostel.models import Room
from utils.base_result import BaseResultWithData
from utils.log_helpers import OperationLogger
from utils.audit.audit_logger import AuditLogger


class RoomCommand:
    
    @staticmethod
    def Create(data, user=None):
        op = OperationLogger("RoomCommand.Create", room_number=data.get('number'))
        op.start()
        try:
            room = Room.objects.create(**data)
            AuditLogger.log_create(Room.__name__, performed_by=user, metadata=data)
            op.success(f"Room {room.number} created successfully")
            return BaseResultWithData(True, "Room created successfully", room, 201)
        except Exception as e:
            op.fail(f"Failed to create room: {str(e)}", exc=e)
            return BaseResultWithData(False, str(e), None, 400)
    
    @staticmethod
    def Update(room_id, data, user=None):
        op = OperationLogger("RoomCommand.Update", room_id=room_id)
        op.start()
        try:
            room = Room.objects.get(id=room_id)
            old_data = {field: getattr(room, field) for field in data.keys()}
            
            for key, value in data.items():
                setattr(room, key, value)
            room.save()
            
            AuditLogger.log_update(Room.__name__, performed_by=user, old_values=old_data, new_values=data)
            op.success(f"Room {room.number} updated successfully")
            return BaseResultWithData(True, "Room updated successfully", room, 200)
        except Room.DoesNotExist:
            op.fail(f"Room with id {room_id} not found")
            return BaseResultWithData(False, "Room not found", None, 404)
        except Exception as e:
            op.fail(f"Failed to update room: {str(e)}", exc=e)
            return BaseResultWithData(False, str(e), None, 400)
    
    @staticmethod
    def ToggleDelete(room_id, user=None):
        op = OperationLogger("RoomCommand.ToggleDelete", room_id=room_id)
        op.start()
        try:
            room = Room.objects.get(id=room_id)
            old_is_deleted = room.is_deleted
            room.is_deleted = not room.is_deleted
            room.save()
            
            AuditLogger.log_delete(Room.__name__, performed_by=user, metadata={"is_deleted": room.is_deleted})
            op.success(f"Room {room.number} deleted" if room.is_deleted else f"Room {room.number} restored")
            return BaseResultWithData(True, "Room deleted successfully" if room.is_deleted else "Room restored successfully", room, 200)
        except Room.DoesNotExist:
            op.fail(f"Room with id {room_id} not found")
            return BaseResultWithData(False, "Room not found", None, 404)
        except Exception as e:
            op.fail(f"Failed to delete room: {str(e)}", exc=e)
            return BaseResultWithData(False, str(e), None, 400)
