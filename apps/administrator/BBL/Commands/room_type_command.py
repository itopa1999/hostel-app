from http import HTTPStatus
from apps.hostel.models import RoomType
from apps.hostel.serializers import RoomTypeSerializer
from utils.base_result import BaseResultWithData
from utils.log_helpers import OperationLogger
from utils.audit.audit_logger import AuditLogger
from utils.serialization_helpers import serialize_for_audit


class RoomTypeCommand:
    
    @staticmethod
    def Create(data, user=None):
        op = OperationLogger("RoomTypeCommand.Create", room_type_name=data.get('name'))
        op.start()
        
        serializer = RoomTypeSerializer(data=data)
        if not serializer.is_valid():
            op.fail(f"Validation failed: {serializer.errors}")
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.BAD_REQUEST,
                message=f"Validation failed: {serializer.errors}"
            )
        
        try:
            room_type = RoomType.objects.create(**serializer.validated_data)
            AuditLogger.log_create(RoomType.__name__, performed_by=user, metadata=serialize_for_audit(serializer.validated_data))
            op.success(f"RoomType {room_type.name} created successfully")
            result_serializer = RoomTypeSerializer(room_type)
            return BaseResultWithData(
                data=result_serializer.data,
                status_code=HTTPStatus.CREATED,
                message="Room type created successfully"
            )
        except Exception as e:
            op.fail(f"Failed to create room type: {str(e)}", exc=e)
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.BAD_REQUEST,
                message=str(e)
            )
    
    @staticmethod
    def Update(room_type_id, data, user=None):
        op = OperationLogger("RoomTypeCommand.Update", room_type_id=room_type_id)
        op.start()
        
        try:
            room_type = RoomType.objects.get(id=room_type_id)
        except RoomType.DoesNotExist:
            op.fail(f"RoomType with id {room_type_id} not found")
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.NOT_FOUND,
                message="Room type not found"
            )
        
        if room_type.is_deleted:
            op.fail(f"RoomType with id {room_type_id} is deleted and cannot be updated")
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.BAD_REQUEST,
                message="This room type is deleted and cannot be updated until it is restored"
            )
        
        serializer = RoomTypeSerializer(room_type, data=data, partial=True)
        if not serializer.is_valid():
            op.fail(f"Validation failed: {serializer.errors}")
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.BAD_REQUEST,
                message=f"Validation failed: {serializer.errors}"
            )
        
        try:
            old_data = {field: getattr(room_type, field) for field in serializer.validated_data.keys()}
            updated_room_type = serializer.save()
            AuditLogger.log_update(RoomType.__name__, performed_by=user, old_values=serialize_for_audit(old_data), new_values=serialize_for_audit(serializer.validated_data))
            op.success(f"RoomType {updated_room_type.name} updated successfully")
            result_serializer = RoomTypeSerializer(updated_room_type)
            return BaseResultWithData(
                data=result_serializer.data,
                status_code=HTTPStatus.OK,
                message="Room type updated successfully"
            )
        except Exception as e:
            op.fail(f"Failed to update room type: {str(e)}", exc=e)
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.BAD_REQUEST,
                message=str(e)
            )
    
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
            result_serializer = RoomTypeSerializer(room_type)
            return BaseResultWithData(
                data=result_serializer.data,
                status_code=HTTPStatus.OK,
                message="Room type deleted successfully" if room_type.is_deleted else "Room type restored successfully"
            )
        except RoomType.DoesNotExist:
            op.fail(f"RoomType with id {room_type_id} not found")
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.NOT_FOUND,
                message="Room type not found"
            )
        except Exception as e:
            op.fail(f"Failed to delete room type: {str(e)}", exc=e)
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.BAD_REQUEST,
                message=str(e)
            )
