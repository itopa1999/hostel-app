from django.db import transaction
from django.utils.timezone import now
from apps.hostel.models import Hotel
from apps.administrator.serializers import HotelUpdateSerializer
from utils.audit.audit_logger import AuditLogger
from utils.enums import AuditAction
from utils.base_result import BaseResultWithData
import logging

logger = logging.getLogger(__name__)


class HotelCommand:
    """Hotel CRUD operations with audit logging"""
        
    @staticmethod
    def Update(hotel_id, data, user=None):
        """
        Update an existing hotel with partial updates and audit logging
        
        Args:
            hotel_id: ID of the hotel to update
            data: Dictionary containing fields to update
            user: User object (from request)
        
        Returns:
            BaseResultWithData with updated hotel data or error message
        """
        try:
            try:
                hotel = Hotel.objects.get(id=hotel_id, is_deleted=False)
            except Hotel.DoesNotExist:
                logger.warning(f"Hotel not found: {hotel_id}")
                
                AuditLogger.log_failure(
                    action=AuditAction.UPDATE.value,
                    entity='Hotel',
                    description=f"Hotel update failed - Hotel not found (ID: {hotel_id})",
                    performed_by=user,
                    metadata={'hotel_id': hotel_id}
                )
                
                return BaseResultWithData(
                    message="Hotel not found",
                    status_code=404,
                    data=None
                )
            
            serializer = HotelUpdateSerializer(hotel, data=data, partial=True)
            
            if not serializer.is_valid():
                error_msg = f"Validation failed: {serializer.errors}"
                logger.warning(f"Hotel update validation error: {error_msg}")
                
                AuditLogger.log_failure(
                    action=AuditAction.UPDATE.value,
                    entity='Hotel',
                    description=f"Hotel update failed - Validation error",
                    performed_by=user,
                    metadata={'errors': serializer.errors, 'attempted_updates': data}
                )
                
                return BaseResultWithData(
                    message=error_msg,
                    status_code=400,
                    data=None
                )
            
            # Store old values for audit
            old_values = {}
            for field in serializer.validated_data.keys():
                old_values[field] = getattr(hotel, field)
            
            with transaction.atomic():
                updated_hotel = serializer.save()
                logger.info(f"Hotel updated successfully: {updated_hotel.id_number}")
                
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
                    message="Hotel updated successfully",
                    status_code=200,
                    data=result_data
                )
        
        except Exception as e:
            logger.error(f"Hotel update error: {str(e)}", exc_info=True)
            
            AuditLogger.log_failure(
                action=AuditAction.UPDATE.value,
                entity='Hotel',
                description=f"Hotel update failed - {str(e)}",
                performed_by=user,
                metadata={'error': str(e), 'hotel_id': hotel_id, 'attempted_updates': data}
            )
            
            return BaseResultWithData(
                message=f"Hotel update failed: {str(e)}",
                status_code=500,
                data=None
            )