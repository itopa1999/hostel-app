from http import HTTPStatus
from apps.hostel.models import Room
from apps.hostel.serializers import RoomSerializer
from utils.base_result import BaseResultWithData
from utils.log_helpers import OperationLogger
from utils.audit.audit_logger import AuditLogger
from utils.serialization_helpers import serialize_for_audit


class RoomCommand:
    
    @staticmethod
    def Create(data, user=None):
        op = OperationLogger("RoomCommand.Create", room_number=data.get('number'))
        op.start()
        
        # Check if room_type is deleted
        if 'room_type' in data:
            from apps.hostel.models import RoomType
            try:
                room_type = RoomType.objects.get(id=data['room_type'])
                if room_type.is_deleted:
                    op.fail(f"Room type with id {data['room_type']} is deleted")
                    return BaseResultWithData(
                        data=None,
                        status_code=HTTPStatus.BAD_REQUEST,
                        message="The selected room type is deleted. Please select another room type or restore the deleted one"
                    )
            except RoomType.DoesNotExist:
                op.fail(f"Room type with id {data['room_type']} not found")
                return BaseResultWithData(
                    data=None,
                    status_code=HTTPStatus.NOT_FOUND,
                    message="Room type not found"
                )
        
        # Check if floor is deleted
        if 'floor' in data and data['floor']:
            from apps.hostel.models import Floor
            try:
                floor = Floor.objects.get(id=data['floor'])
                if floor.is_deleted:
                    op.fail(f"Floor with id {data['floor']} is deleted")
                    return BaseResultWithData(
                        data=None,
                        status_code=HTTPStatus.BAD_REQUEST,
                        message="The selected floor is deleted. Please select another floor or restore the deleted one"
                    )
            except Floor.DoesNotExist:
                op.fail(f"Floor with id {data['floor']} not found")
                return BaseResultWithData(
                    data=None,
                    status_code=HTTPStatus.NOT_FOUND,
                    message="Floor not found"
                )
        
        serializer = RoomSerializer(data=data)
        if not serializer.is_valid():
            op.fail(f"Validation failed: {serializer.errors}")
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.BAD_REQUEST,
                message=f"Validation failed: {serializer.errors}"
            )
        
        try:
            room = Room.objects.create(**serializer.validated_data)
            AuditLogger.log_create(Room.__name__, performed_by=user, metadata=serialize_for_audit(serializer.validated_data))
            op.success(f"Room {room.number} created successfully")
            result_serializer = RoomSerializer(room)
            return BaseResultWithData(
                data=result_serializer.data,
                status_code=HTTPStatus.CREATED,
                message="Room created successfully"
            )
        except Exception as e:
            op.fail(f"Failed to create room: {str(e)}", exc=e)
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.BAD_REQUEST,
                message=str(e)
            )
    
    @staticmethod
    def Update(room_id, data, user=None):
        op = OperationLogger("RoomCommand.Update", room_id=room_id)
        op.start()
        
        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            op.fail(f"Room with id {room_id} not found")
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.NOT_FOUND,
                message="Room not found"
            )
        
        if room.is_deleted:
            op.fail(f"Room with id {room_id} is deleted and cannot be updated")
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.BAD_REQUEST,
                message="This room is deleted and cannot be updated until it is restored"
            )
        
        # Check if room_type is being updated and if it's deleted
        if 'room_type' in data:
            from apps.hostel.models import RoomType
            try:
                room_type = RoomType.objects.get(id=data['room_type'])
                if room_type.is_deleted:
                    op.fail(f"Room type with id {data['room_type']} is deleted")
                    return BaseResultWithData(
                        data=None,
                        status_code=HTTPStatus.BAD_REQUEST,
                        message="The selected room type is deleted. Please select another room type or restore the deleted one"
                    )
            except RoomType.DoesNotExist:
                op.fail(f"Room type with id {data['room_type']} not found")
                return BaseResultWithData(
                    data=None,
                    status_code=HTTPStatus.NOT_FOUND,
                    message="Room type not found"
                )
        
        # Check if floor is being updated and if it's deleted
        if 'floor' in data and data['floor']:
            from apps.hostel.models import Floor
            try:
                floor = Floor.objects.get(id=data['floor'])
                if floor.is_deleted:
                    op.fail(f"Floor with id {data['floor']} is deleted")
                    return BaseResultWithData(
                        data=None,
                        status_code=HTTPStatus.BAD_REQUEST,
                        message="The selected floor is deleted. Please select another floor or restore the deleted one"
                    )
            except Floor.DoesNotExist:
                op.fail(f"Floor with id {data['floor']} not found")
                return BaseResultWithData(
                    data=None,
                    status_code=HTTPStatus.NOT_FOUND,
                    message="Floor not found"
                )
        
        serializer = RoomSerializer(room, data=data, partial=True)
        if not serializer.is_valid():
            op.fail(f"Validation failed: {serializer.errors}")
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.BAD_REQUEST,
                message=f"Validation failed: {serializer.errors}"
            )
        
        try:
            old_data = {field: getattr(room, field) for field in serializer.validated_data.keys()}
            updated_room = serializer.save()
            AuditLogger.log_update(Room.__name__, performed_by=user, old_values=serialize_for_audit(old_data), new_values=serialize_for_audit(serializer.validated_data))
            op.success(f"Room {updated_room.number} updated successfully")
            result_serializer = RoomSerializer(updated_room)
            return BaseResultWithData(
                data=result_serializer.data,
                status_code=HTTPStatus.OK,
                message="Room updated successfully"
            )
        except Exception as e:
            op.fail(f"Failed to update room: {str(e)}", exc=e)
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.BAD_REQUEST,
                message=str(e)
            )
    
    @staticmethod
    def ToggleDelete(room_id, user=None):
        op = OperationLogger("RoomCommand.ToggleDelete", room_id=room_id)
        op.start()
        try:
            room = Room.objects.get(id=room_id)
            room.is_deleted = not room.is_deleted
            room.save()
            
            AuditLogger.log_delete(Room.__name__, performed_by=user, metadata={"is_deleted": room.is_deleted})
            op.success(f"Room {room.number} deleted" if room.is_deleted else f"Room {room.number} restored")
            result_serializer = RoomSerializer(room)
            return BaseResultWithData(
                data=result_serializer.data,
                status_code=HTTPStatus.OK,
                message="Room deleted successfully" if room.is_deleted else "Room restored successfully"
            )
        except Room.DoesNotExist:
            op.fail(f"Room with id {room_id} not found")
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.NOT_FOUND,
                message="Room not found"
            )
        except Exception as e:
            op.fail(f"Failed to delete room: {str(e)}", exc=e)
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.BAD_REQUEST,
                message=str(e)
            )
