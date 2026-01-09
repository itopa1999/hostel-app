from apps.hostel.models import RoomType
from utils.base_result import BaseResultWithData
from utils.log_helpers import OperationLogger
from utils.audit.audit_logger import AuditLogger


class RoomTypeCommand:
    
    @staticmethod
    def Create(data, user=None):
        op = OperationLogger("RoomTypeCommand.Create", room_type_name=data.get('name'))
        op.start()
        try:
            room_type = RoomType.objects.create(**data)
            AuditLogger.log_create(RoomType.__name__, performed_by=user, metadata=data)
            op.success(f"RoomType {room_type.name} created successfully")
            return BaseResultWithData(True, "Room type created successfully", room_type, 201)
        except Exception as e:
            op.fail(f"Failed to create room type: {str(e)}", exc=e)
            return BaseResultWithData(False, str(e), None, 400)
    
    @staticmethod
    def Update(room_type_id, data, user=None):
        op = OperationLogger("RoomTypeCommand.Update", room_type_id=room_type_id)
        op.start()
        try:
            room_type = RoomType.objects.get(id=room_type_id)
            old_data = {field: getattr(room_type, field) for field in data.keys()}
            
            for key, value in data.items():
                setattr(room_type, key, value)
            room_type.save()
            
            AuditLogger.log_update(RoomType.__name__, performed_by=user, old_values=old_data, new_values=data)
            op.success(f"RoomType {room_type.name} updated successfully")
            return BaseResultWithData(True, "Room type updated successfully", room_type, 200)
        except RoomType.DoesNotExist:
            op.fail(f"RoomType with id {room_type_id} not found")
            return BaseResultWithData(False, "Room type not found", None, 404)
        except Exception as e:
            op.fail(f"Failed to update room type: {str(e)}", exc=e)
            return BaseResultWithData(False, str(e), None, 400)
    
    @staticmethod
    def ToggleDelete(room_type_id, user=None):
        op = OperationLogger("RoomTypeCommand.ToggleDelete", room_type_id=room_type_id)
        op.start()
        try:
            room_type = RoomType.objects.get(id=room_type_id)
            old_is_deleted = room_type.is_deleted
            room_type.is_deleted = not room_type.is_deleted
            room_type.save()
            
            AuditLogger.log_delete(RoomType.__name__, performed_by=user, metadata={"is_deleted": room_type.is_deleted})
            op.success(f"RoomType {room_type.name} deleted" if room_type.is_deleted else f"RoomType {room_type.name} restored")
            return BaseResultWithData(True, "Room type deleted successfully" if room_type.is_deleted else "Room type restored successfully", room_type, 200)
        except RoomType.DoesNotExist:
            op.fail(f"RoomType with id {room_type_id} not found")
            return BaseResultWithData(False, "Room type not found", None, 404)
        except Exception as e:
            op.fail(f"Failed to delete room type: {str(e)}", exc=e)
            return BaseResultWithData(False, str(e), None, 400)
