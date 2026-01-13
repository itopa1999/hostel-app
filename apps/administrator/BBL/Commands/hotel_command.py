from django.db import transaction
from django.utils.timezone import now
from http import HTTPStatus
from apps.hostel.models import Hotel
from apps.administrator.serializers import HotelUpdateSerializer
from utils.audit.audit_logger import AuditLogger
from utils.enums import AuditAction
from utils.base_result import BaseResultWithData
from utils.log_helpers import OperationLogger


class HotelCommand:
    """Hotel CRUD operations with audit logging"""
        
    @staticmethod
    def Update(data, user=None):
        """
        Update an existing hotel with partial updates and audit logging
        
        Args:
            data: Dictionary containing fields to update
            user: User object (from request)
        
        Returns:
            BaseResultWithData with updated hotel data or error message
        """
        
        op = OperationLogger(
            "HotelCommand.Update",
            username=user.username if user else "Anonymous"
        )
        op.start()
        
        try:
            try:
                hotel = Hotel.objects.filter(is_deleted=False).first()
            except Hotel.DoesNotExist:
                op.fail(f"Hotel not found")
                
                AuditLogger.log_failure(
                    'CHANGE_PASSWORD',
                    'Hotel',
                    performed_by=user,
                    description=f"Hotel update failed - Hotel not found"
                )
                
                return BaseResultWithData(
                    data=None,
                    status_code=HTTPStatus.NOT_FOUND,
                    message="Hotel not found"
                )
            
            serializer = HotelUpdateSerializer(hotel, data=data, partial=True)
            
            if not serializer.is_valid():
                error_msg = f"Validation failed: {serializer.errors}"
                op.fail(f"Hotel update validation error: {error_msg}")
                
                AuditLogger.log_failure(
                    'UPDATE',
                    'Hotel',
                    performed_by=user,
                    description=f"Hotel update failed - Validation error",
                    metadata={'errors': serializer.errors, 'attempted_updates': data}
                )
                
                return BaseResultWithData(
                    data=None,
                    status_code=HTTPStatus.BAD_REQUEST,
                    message=error_msg
                )
            
            # Store old values for audit
            old_values = {}
            for field in serializer.validated_data.keys():
                old_values[field] = getattr(hotel, field)
            
            with transaction.atomic():
                updated_hotel = serializer.save()
                op.success(f"Hotel updated successfully: {updated_hotel.id_number}")
                
                AuditLogger.log_update(
                    entity='Hotel',
                    description=f"Hotel '{updated_hotel.name}' updated",
                    performed_by=user,
                    old_values=old_values,
                    new_values=serializer.validated_data
                )
                
                result_data = {
                    'id': updated_hotel.id,
                    'name': updated_hotel.name,
                    'id_number': updated_hotel.id_number,
                    'address': updated_hotel.address,
                    'city': updated_hotel.city,
                    'country': updated_hotel.country,
                    'postal_code': updated_hotel.postal_code,
                    'phone': updated_hotel.phone,
                    'email': updated_hotel.email,
                    'check_in_time': str(updated_hotel.check_in_time),
                    'check_out_time': str(updated_hotel.check_out_time),
                }
                
                return BaseResultWithData(
                    data=result_data,
                    status_code=HTTPStatus.OK,
                    message="Hotel updated successfully"
                )
        
        except Exception as e:
            op.fail(f"Hotel update error: {str(e)}", exc=e)
            
            AuditLogger.log_failure(
                'UPDATE',
                'Hotel',
                performed_by=user,
                description=f"Hotel update failed - {str(e)}",
                metadata={'error': str(e)}
            )
            
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                message=f"Hotel update failed: {str(e)}"
            )