from http import HTTPStatus
from apps.hostel.models import Floor
from apps.hostel.serializers import FloorSerializer
from utils.base_result import BaseResultWithData
from utils.log_helpers import OperationLogger
from utils.audit.audit_logger import AuditLogger
from utils.serialization_helpers import serialize_for_audit


class FloorCommand:
    
    @staticmethod
    def Create(data, user=None):
        op = OperationLogger("FloorCommand.Create", floor_number=data.get('number'))
        op.start()
        
        serializer = FloorSerializer(data=data)
        if not serializer.is_valid():
            op.fail(f"Validation failed: {serializer.errors}")
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.BAD_REQUEST,
                message=f"Validation failed: {serializer.errors}"
            )
        
        try:
            floor = Floor.objects.create(**serializer.validated_data)
            AuditLogger.log_create(Floor.__name__, performed_by=user, metadata=serialize_for_audit(serializer.validated_data))
            op.success(f"Floor {floor.number} created successfully")
            result_serializer = FloorSerializer(floor)
            return BaseResultWithData(
                data=result_serializer.data,
                status_code=HTTPStatus.CREATED,
                message="Floor created successfully"
            )
        except Exception as e:
            op.fail(f"Failed to create floor: {str(e)}", exc=e)
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.BAD_REQUEST,
                message=str(e)
            )
    
    @staticmethod
    def Update(floor_id, data, user=None):
        op = OperationLogger("FloorCommand.Update", floor_id=floor_id)
        op.start()
        
        try:
            floor = Floor.objects.get(id=floor_id)
        except Floor.DoesNotExist:
            op.fail(f"Floor with id {floor_id} not found")
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.NOT_FOUND,
                message="Floor not found"
            )
        
        if floor.is_deleted:
            op.fail(f"Floor with id {floor_id} is deleted and cannot be updated")
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.BAD_REQUEST,
                message="This floor is deleted and cannot be updated until it is restored"
            )
        
        serializer = FloorSerializer(floor, data=data, partial=True)
        if not serializer.is_valid():
            op.fail(f"Validation failed: {serializer.errors}")
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.BAD_REQUEST,
                message=f"Validation failed: {serializer.errors}"
            )
        
        try:
            old_data = {field: getattr(floor, field) for field in serializer.validated_data.keys()}
            updated_floor = serializer.save()
            AuditLogger.log_update(Floor.__name__, performed_by=user, old_values=serialize_for_audit(old_data), new_values=serialize_for_audit(serializer.validated_data))
            op.success(f"Floor {updated_floor.number} updated successfully")
            result_serializer = FloorSerializer(updated_floor)
            return BaseResultWithData(
                data=result_serializer.data,
                status_code=HTTPStatus.OK,
                message="Floor updated successfully"
            )
        except Exception as e:
            op.fail(f"Failed to update floor: {str(e)}", exc=e)
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.BAD_REQUEST,
                message=str(e)
            )
    
    @staticmethod
    def ToggleDelete(floor_id, user=None):
        op = OperationLogger("FloorCommand.ToggleDelete", floor_id=floor_id)
        op.start()
        try:
            floor = Floor.objects.get(id=floor_id)
            old_is_deleted = floor.is_deleted
            floor.is_deleted = not floor.is_deleted
            floor.save()
            
            AuditLogger.log_delete(Floor.__name__, performed_by=user, metadata={"is_deleted": floor.is_deleted})
            op.success(f"Floor {floor.number} deleted" if floor.is_deleted else f"Floor {floor.number} restored")
            result_serializer = FloorSerializer(floor)
            return BaseResultWithData(
                data=result_serializer.data,
                status_code=HTTPStatus.OK,
                message="Floor deleted successfully" if floor.is_deleted else "Floor restored successfully"
            )
        except Floor.DoesNotExist:
            op.fail(f"Floor with id {floor_id} not found")
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.NOT_FOUND,
                message="Floor not found"
            )
        except Exception as e:
            op.fail(f"Failed to delete floor: {str(e)}", exc=e)
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.BAD_REQUEST,
                message=str(e)
            )
