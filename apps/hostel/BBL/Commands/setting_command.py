from http import HTTPStatus
from django.db import transaction
from utils.base_result import BaseResultWithData
from utils.log_helpers import OperationLogger
from apps.hostel.models import Setting
from apps.hostel.serializers import SettingSerializer
from utils.audit.audit_logger import AuditLogger


class SettingCommand:
    """Handle update operations for Settings"""
    
    @staticmethod
    def Update(data, performed_by=None):
        """
        Update general settings (tax and discount percentages).
        
        Args:
            data (dict): Settings data (tax_percentage, default_discount_percentage, description)
            performed_by (User): User performing the action
            
        Returns:
            BaseResultWithData: Result with updated settings data
        """
        op = OperationLogger("SettingCommand.Update")
        op.start()
        
        try:
            tax_percentage = data.get('tax_percentage')
            discount_percentage = data.get('default_discount_percentage')
            description = data.get('description', '')
            
            # Validate tax percentage
            if tax_percentage is not None:
                try:
                    tax_percentage = float(tax_percentage)
                    if tax_percentage < 0 or tax_percentage > 100:
                        op.fail("Tax percentage must be between 0 and 100")
                        return BaseResultWithData(
                            message="Tax percentage must be between 0 and 100",
                            status_code=HTTPStatus.BAD_REQUEST
                        )
                except (ValueError, TypeError):
                    op.fail("Invalid tax percentage format")
                    return BaseResultWithData(
                        message="Invalid tax percentage",
                        status_code=HTTPStatus.BAD_REQUEST
                    )
            
            # Validate discount percentage
            if discount_percentage is not None:
                try:
                    discount_percentage = float(discount_percentage)
                    if discount_percentage < 0 or discount_percentage > 100:
                        op.fail("Discount percentage must be between 0 and 100")
                        return BaseResultWithData(
                            message="Discount percentage must be between 0 and 100",
                            status_code=HTTPStatus.BAD_REQUEST
                        )
                except (ValueError, TypeError):
                    op.fail("Invalid discount percentage format")
                    return BaseResultWithData(
                        message="Invalid discount percentage",
                        status_code=HTTPStatus.BAD_REQUEST
                    )
            
            with transaction.atomic():
                # Get current settings
                setting = Setting.get_settings()
                
                # Store old values for audit
                old_values = {
                    "tax_percentage": float(setting.tax_percentage),
                    "default_discount_percentage": float(setting.default_discount_percentage),
                    "description": setting.description
                }
                
                # Update fields
                if tax_percentage is not None:
                    setting.tax_percentage = tax_percentage
                if discount_percentage is not None:
                    setting.default_discount_percentage = discount_percentage
                if description:
                    setting.description = description
                
                setting.modified_by = performed_by.username if performed_by else None
                setting.save()
                
                op.success("Settings updated successfully")
                
                # Store new values for audit
                new_values = {
                    "tax_percentage": float(setting.tax_percentage),
                    "default_discount_percentage": float(setting.default_discount_percentage),
                    "description": setting.description
                }
                
                AuditLogger.log_update(
                    'Setting',
                    performed_by=performed_by,
                    old_values=old_values,
                    new_values=new_values,
                    description=f"Updated system settings - Tax: {setting.tax_percentage}%, Discount: {setting.default_discount_percentage}%"
                )
                
                serializer = SettingSerializer(setting)
                return BaseResultWithData(
                    message="Settings updated successfully",
                    data=serializer.data,
                    status_code=HTTPStatus.OK
                )
        except Exception as e:
            op.fail(f"Failed to update settings: {str(e)}", exc=e)
            AuditLogger.log_failure(
                'UPDATE_SETTINGS',
                'Setting',
                performed_by=performed_by,
                description=f"Failed to update settings - {str(e)}"
            )
            return BaseResultWithData(
                message=str(e),
                status_code=HTTPStatus.BAD_REQUEST
            )
