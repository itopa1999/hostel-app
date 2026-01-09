from django.conf import settings
from django.contrib.auth import authenticate
from urllib.parse import urlencode
from rest_framework_simplejwt.tokens import RefreshToken
from http import HTTPStatus

from utils.base_result import BaseResultWithData
from utils.log_helpers import OperationLogger
from utils.audit.audit_logger import AuditLogger


class LoginCommand:
    """Handle username/password login"""
    
    @staticmethod
    def Execute(username, password, group_id, request=None):
        """
        Authenticate user with username and password.
        
        Args:
            username (str): Username
            password (str): Password
            group_id (int): Group ID for additional validation
            request: HTTP request object (optional)
                        
        Returns:
            BaseResultWithData: Result with tokens and user info
        """
        op = OperationLogger(
            "LoginCommand",
            username=username
        )
        op.start()
        
        # Validate group_id is provided
        if not group_id:
            op.fail(f"Group ID is required for login")
            AuditLogger.log_failure(
                'LOGIN',
                'User',
                description=f"Failed login attempt for username {username} - Group ID not provided"
            )
            return BaseResultWithData(
                message="Group ID is required",
                status_code=HTTPStatus.BAD_REQUEST
            )
        
        # Authenticate user
        user = authenticate(username=username, password=password)
        
        if not user:
            op.fail(f"Invalid credentials for user {username}")
            AuditLogger.log_failure(
                'LOGIN',
                'User',
                description=f"Failed login attempt for username {username} - Invalid credentials"
            )
            return BaseResultWithData(
                message="Invalid username or password",
                status_code=HTTPStatus.UNAUTHORIZED
            )
        
        # Check if user is soft deleted
        if user.is_deleted:
            op.fail(f"User {username} has been deleted")
            AuditLogger.log_failure(
                'LOGIN',
                'User',
                performed_by=user,
                target_user=user,
                description=f"Failed login attempt for user {user.username} - Account deleted"
            )
            return BaseResultWithData(
                message="User account not found",
                status_code=HTTPStatus.UNAUTHORIZED
            )
        
        if not user.is_active:
            op.fail(f"User {username} is inactive")
            AuditLogger.log_failure(
                'LOGIN',
                'User',
                performed_by=user,
                target_user=user,
                description=f"Failed login attempt for user {user.username} - Account inactive"
            )
            return BaseResultWithData(
                message="User account is inactive",
                status_code=HTTPStatus.FORBIDDEN
            )
        
        # Validate group_id belongs to user
        user_groups = user.groups.values_list('id', flat=True)
        if group_id not in user_groups:
            op.fail(f"User {username} does not belong to group {group_id}")
            AuditLogger.log_failure(
                'LOGIN',
                'User',
                performed_by=user,
                target_user=user,
                description=f"Failed login attempt for user {user.username} - Invalid group {group_id}"
            )
            return BaseResultWithData(
                message="Login failed, user does not belong to the selected group",
                status_code=HTTPStatus.FORBIDDEN
            )
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        
        # Get groups with id and name
        groups = [
            {
                'id': group.id,
                'name': group.name
            }
            for group in user.groups.all()
        ]
        
        op.success(f"Login successful for user {user.id}")
        
        # Log successful login
        metadata = {}
        if request:
            metadata['ip_address'] = request.META.get('REMOTE_ADDR', 'Unknown')
            metadata['user_agent'] = request.META.get('HTTP_USER_AGENT', 'Unknown')
        
        AuditLogger.log_login(
            user=user,
            description=f"User {user.username} logged in successfully",
            metadata=metadata
        )
        
        return BaseResultWithData(
            message="Login successful",
            data={
                "access": access_token,
                "refresh": refresh_token,
                "email": user.email,
                "username": user.username,
                "name": f"{user.first_name} {user.last_name}",
                "id_number": user.id_number,
                "groups": groups,
                "is_staff": user.is_staff,
                "is_superuser": user.is_superuser,
            },
            status_code=HTTPStatus.OK
        )
