from http import HTTPStatus
from utils.base_result import BaseResultWithData
from utils.log_helpers import OperationLogger
from apps.hostel.models import Setting
from apps.hostel.serializers import SettingSerializer
from utils.audit.audit_logger import AuditLogger
from utils.cache_helper import GlobalCache
from utils.enums import CacheKeys


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
            # Try to get from cache first
            cached_setting = GlobalCache.get(CacheKeys.SETTINGS_GENERAL.value)
            if cached_setting:
                op.success("Settings retrieved successfully (cached)")
                return BaseResultWithData(
                    message="Settings retrieved successfully (cached)",
                    data=cached_setting,
                    status_code=HTTPStatus.OK
                )
            
            setting = Setting.get_settings()
            op.success("Settings retrieved successfully")
            
            serializer = SettingSerializer(setting)
            
            # Cache the result
            GlobalCache.set(CacheKeys.SETTINGS_GENERAL.value, serializer.data)
            
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
