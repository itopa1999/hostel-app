from http import HTTPStatus
from apps.hostel.models import GuestProfile
from apps.hostel.serializers import GuestProfileSerializer
from utils.base_result import BaseResultWithData
from utils.log_helpers import OperationLogger
from utils.audit.audit_logger import AuditLogger
from utils.serialization_helpers import serialize_for_audit


class GuestProfileCommand:
    
    @staticmethod
    def Create(data, user=None):
        op = OperationLogger("GuestProfileCommand.Create", guest_name=data.get('name'))
        op.start()
        
        serializer = GuestProfileSerializer(data=data)
        if not serializer.is_valid():
            op.fail(f"Validation failed: {serializer.errors}")
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.BAD_REQUEST,
                message=f"Validation failed: {serializer.errors}"
            )
        
        try:
            guest = GuestProfile.objects.create(**serializer.validated_data)
            AuditLogger.log_create(GuestProfile.__name__, performed_by=user, metadata=serialize_for_audit(serializer.validated_data))
            op.success(f"Guest profile {guest.name} created successfully")
            result_serializer = GuestProfileSerializer(guest)
            return BaseResultWithData(
                data=result_serializer.data,
                status_code=HTTPStatus.CREATED,
                message="Guest profile created successfully"
            )
        except Exception as e:
            op.fail(f"Failed to create guest profile: {str(e)}", exc=e)
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.BAD_REQUEST,
                message=str(e)
            )
    
    @staticmethod
    def Update(guest_id, data, user=None):
        op = OperationLogger("GuestProfileCommand.Update", guest_id=guest_id)
        op.start()
        
        try:
            guest = GuestProfile.objects.get(id=guest_id)
        except GuestProfile.DoesNotExist:
            op.fail(f"Guest profile with id {guest_id} not found")
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.NOT_FOUND,
                message="Guest profile not found"
            )
        
        if guest.is_deleted:
            op.fail(f"Guest profile with id {guest_id} is deleted and cannot be updated")
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.BAD_REQUEST,
                message="This guest profile is deleted and cannot be updated until it is restored"
            )
        
        serializer = GuestProfileSerializer(guest, data=data, partial=True)
        if not serializer.is_valid():
            op.fail(f"Validation failed: {serializer.errors}")
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.BAD_REQUEST,
                message=f"Validation failed: {serializer.errors}"
            )
        
        try:
            old_data = {field: getattr(guest, field) for field in serializer.validated_data.keys()}
            updated_guest = serializer.save()
            AuditLogger.log_update(GuestProfile.__name__, performed_by=user, old_values=serialize_for_audit(old_data), new_values=serialize_for_audit(serializer.validated_data))
            op.success(f"Guest profile {updated_guest.name} updated successfully")
            result_serializer = GuestProfileSerializer(updated_guest)
            return BaseResultWithData(
                data=result_serializer.data,
                status_code=HTTPStatus.OK,
                message="Guest profile updated successfully"
            )
        except Exception as e:
            op.fail(f"Failed to update guest profile: {str(e)}", exc=e)
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.BAD_REQUEST,
                message=str(e)
            )
    
    @staticmethod
    def ToggleDelete(guest_id, user=None):
        op = OperationLogger("GuestProfileCommand.ToggleDelete", guest_id=guest_id)
        op.start()
        try:
            guest = GuestProfile.objects.get(id=guest_id)
            guest.is_deleted = not guest.is_deleted
            guest.save()
            
            AuditLogger.log_delete(GuestProfile.__name__, performed_by=user, metadata={"is_deleted": guest.is_deleted})
            op.success(f"Guest profile {guest.name} deleted" if guest.is_deleted else f"Guest profile {guest.name} restored")
            result_serializer = GuestProfileSerializer(guest)
            return BaseResultWithData(
                data=result_serializer.data,
                status_code=HTTPStatus.OK,
                message="Guest profile deleted successfully" if guest.is_deleted else "Guest profile restored successfully"
            )
        except GuestProfile.DoesNotExist:
            op.fail(f"Guest profile with id {guest_id} not found")
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.NOT_FOUND,
                message="Guest profile not found"
            )
        except Exception as e:
            op.fail(f"Failed to delete guest profile: {str(e)}", exc=e)
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.BAD_REQUEST,
                message=str(e)
            )
