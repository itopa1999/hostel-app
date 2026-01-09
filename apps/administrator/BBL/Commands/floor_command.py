from apps.hostel.models import Floor
from utils.base_result import BaseResultWithData
from utils.log_helpers import OperationLogger
from utils.audit.audit_logger import AuditLogger


class FloorCommand:
    
    @staticmethod
    def Create(data, user=None):
        op = OperationLogger("FloorCommand.Create", floor_number=data.get('number'))
        op.start()
        try:
            floor = Floor.objects.create(**data)
            AuditLogger.log_create(Floor.__name__, performed_by=user, metadata=data)
            op.success(f"Floor {floor.number} created successfully")
            return BaseResultWithData(True, "Floor created successfully", floor, 201)
        except Exception as e:
            op.fail(f"Failed to create floor: {str(e)}", exc=e)
            return BaseResultWithData(False, str(e), None, 400)
    
    @staticmethod
    def Update(floor_id, data, user=None):
        op = OperationLogger("FloorCommand.Update", floor_id=floor_id)
        op.start()
        try:
            floor = Floor.objects.get(id=floor_id)
            old_data = {field: getattr(floor, field) for field in data.keys()}
            
            for key, value in data.items():
                setattr(floor, key, value)
            floor.save()
            
            AuditLogger.log_update(Floor.__name__, performed_by=user, old_values=old_data, new_values=data)
            op.success(f"Floor {floor.number} updated successfully")
            return BaseResultWithData(True, "Floor updated successfully", floor, 200)
        except Floor.DoesNotExist:
            op.fail(f"Floor with id {floor_id} not found")
            return BaseResultWithData(False, "Floor not found", None, 404)
        except Exception as e:
            op.fail(f"Failed to update floor: {str(e)}", exc=e)
            return BaseResultWithData(False, str(e), None, 400)
    
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
            return BaseResultWithData(True, "Floor deleted successfully" if floor.is_deleted else "Floor restored successfully", floor, 200)
        except Floor.DoesNotExist:
            op.fail(f"Floor with id {floor_id} not found")
            return BaseResultWithData(False, "Floor not found", None, 404)
        except Exception as e:
            op.fail(f"Failed to delete floor: {str(e)}", exc=e)
            return BaseResultWithData(False, str(e), None, 400)
