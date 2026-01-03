from http import HTTPStatus
from django.db.models import Q
from django.db import transaction
from utils.base_result import BaseResultWithData
from utils.log_helpers import OperationLogger
from apps.users.models import User
from apps.users.serializers import UserSerializer



class UserCommand:
    """Handle CRUD operations for User"""
    
    @staticmethod
    def Create(username, first_name, last_name, password, groups, email=None, request=None):
        """
        Create a new user.
        
        Args:
            username (str): Username (required)
            first_name (str): First name (required)
            last_name (str): Last name (required)
            password (str): Password (required)
            groups (list): List of Group objects (required)
            email (str): Email address (optional)
            
        Returns:
            BaseResultWithData: Result with created user data
        """
        op = OperationLogger(
            "UserCommand.Create",
            username=username,
            email=email
        )
        op.start()
        
        # Validate required fields
        if not all([username, first_name, last_name, password, groups]):
            op.fail("Missing required fields: username, first_name, last_name, password, groups")
            return BaseResultWithData(
                message="username, first_name, last_name, password, and groups are required",
                status_code=HTTPStatus.BAD_REQUEST
            )
        
        # Check if user already exists
        if User.objects.filter(username=username, is_deleted=False).exists():
            op.fail(f"User {username} already exists")
            return BaseResultWithData(
                message="Username already exists",
                status_code=HTTPStatus.BAD_REQUEST
            )
        
        # Check email only if provided
        if email and User.objects.filter(email=email, is_deleted=False).exists():
            op.fail(f"Email {email} already exists")
            return BaseResultWithData(
                message="Email already exists",
                status_code=HTTPStatus.BAD_REQUEST
            )
            
        with transaction.atomic():
        
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password,
            )
            
            # Assign groups (required)
            user.groups.set(groups)
            
            op.success(f"User {username} created successfully")
            return BaseResultWithData(
                message="User created successfully",
                data=UserSerializer(user).data,
                status_code=HTTPStatus.CREATED
            )
    
    
    @staticmethod
    def changePassword(user_id, old_password, new_password):
        """
        Change user password.
        
        Args:
            user_id (int): User ID (required)
            old_password (str): Current password (required)
            new_password (str): New password (required)
            
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
            return BaseResultWithData(
                message="user_id, old_password, and new_password are required",
                status_code=HTTPStatus.BAD_REQUEST
            )
        
        try:
            user = User.objects.get(id=user_id, is_deleted=False)
            
            # Verify old password
            if not user.check_password(old_password):
                op.fail(f"Invalid old password for user {user_id}")
                return BaseResultWithData(
                    message="Invalid old password",
                    status_code=HTTPStatus.UNAUTHORIZED
                )
            
            # Check if new password is the same as old password
            if old_password == new_password:
                op.fail(f"New password must be different from old password")
                return BaseResultWithData(
                    message="New password must be different from old password",
                    status_code=HTTPStatus.BAD_REQUEST
                )
            
            # Update password
            with transaction.atomic():
                user.set_password(new_password)
                user.save(update_fields=['password'])
            
            op.success(f"Password changed successfully for user {user_id}")
            return BaseResultWithData(
                message="Password changed successfully",
                status_code=HTTPStatus.OK
            )
            
        except User.DoesNotExist:
            op.fail("User not found")
            return BaseResultWithData(
                message="User not found",
                status_code=HTTPStatus.NOT_FOUND
            )
