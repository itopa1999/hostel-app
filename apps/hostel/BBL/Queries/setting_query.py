from http import HTTPStatus
from utils.base_result import BaseResultWithData
from utils.log_helpers import OperationLogger
from apps.hostel.models import Setting
from apps.hostel.serializers import SettingSerializer
from utils.audit.audit_logger import AuditLogger


class SettingQuery:
    """Handle read operations for Settings"""
    
    @staticmethod
    def Get():
        """
        Get current general settings.
        
        Returns:
            BaseResultWithData: Result with settings data
        """
        op = OperationLogger("SettingQuery.Get")
        op.start()
        
        try:
            setting = Setting.get_settings()
            op.success("Settings retrieved successfully")
            
            serializer = SettingSerializer(setting)
            return BaseResultWithData(
                message="Settings retrieved successfully",
                data=serializer.data,
                status_code=HTTPStatus.OK
            )
        except Exception as e:
            op.fail(f"Failed to retrieve settings: {str(e)}", exc=e)
            AuditLogger.log_failure(
                'GET_SETTINGS',
                'Setting',
                description=f"Failed to retrieve settings - {str(e)}"
            )
            return BaseResultWithData(
                message=str(e),
                status_code=HTTPStatus.BAD_REQUEST
            )
