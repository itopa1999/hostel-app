from http import HTTPStatus
from django.db.models import Q
from django.db import transaction
from utils.base_result import BaseResultWithData
from utils.log_helpers import OperationLogger
from apps.users.models import User
from utils.audit.audit_logger import AuditLogger


class UserCommand:
    """Handle CRUD operations for User"""
    
    @staticmethod
    def changePassword(user_id, old_password, new_password, performed_by=None):
        """
        Change user password.
        
        Args:
            user_id (int): User ID (required)
            old_password (str): Current password (required)
            new_password (str): New password (required)
            performed_by (User): User performing the action (optional)
            
        Returns:
            BaseResultWithData: Result with success message
        """
        op = OperationLogger(
            "UserCommand.changePassword",
            user_id=user_id
        )
        op.start()
        
        # Validate required fields
        if not all([user_id, old_password, new_password]):
            op.fail("Missing required fields: user_id, old_password, new_password")
            AuditLogger.log_failure(
                'CHANGE_PASSWORD',
                'User',
                performed_by=performed_by,
                description=f"Failed to change password for user {user_id} - Missing required fields"
            )
            return BaseResultWithData(
                message="user_id, old_password, and new_password are required",
                status_code=HTTPStatus.BAD_REQUEST
            )
        
        try:
            user = User.objects.get(id=user_id, is_deleted=False)
            
            # Verify old password
            if not user.check_password(old_password):
                op.fail(f"Invalid old password for user {user_id}")
                AuditLogger.log_failure(
                    'CHANGE_PASSWORD',
                    'User',
                    target_user=user,
                    performed_by=performed_by or user,
                    description=f"Failed to change password for user {user.username} - Invalid old password"
                )
                return BaseResultWithData(
                    message="Invalid old password",
                    status_code=HTTPStatus.UNAUTHORIZED
                )
            
            # Check if new password is the same as old password
            if old_password == new_password:
                op.fail(f"New password must be different from old password")
                AuditLogger.log_failure(
                    'CHANGE_PASSWORD',
                    'User',
                    target_user=user,
                    performed_by=performed_by or user,
                    description=f"Failed to change password for user {user.username} - Password same as old password"
                )
                return BaseResultWithData(
                    message="New password must be different from old password",
                    status_code=HTTPStatus.BAD_REQUEST
                )
            
            # Update password
            with transaction.atomic():
                user.set_password(new_password)
                user.save(update_fields=['password'])
            
            op.success(f"Password changed successfully for user {user_id}")
            
            # Log audit
            AuditLogger.log_password_change(
                user=user,
                performed_by=performed_by or user,
                description=f"Password changed for user {user.username}"
            )
            
            return BaseResultWithData(
                message="Password changed successfully",
                status_code=HTTPStatus.OK
            )
            
        except User.DoesNotExist:
            op.fail("User not found")
            AuditLogger.log_failure(
                'CHANGE_PASSWORD',
                'User',
                performed_by=performed_by,
                description=f"Failed to change password for user {user_id} - User not found"
            )
            return BaseResultWithData(
                message="User not found",
                status_code=HTTPStatus.NOT_FOUND
            )
