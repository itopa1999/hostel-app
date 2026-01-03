from http import HTTPStatus
from django.db.models import Q
from django.db import transaction
from utils.base_result import BaseResultWithData
from utils.log_helpers import OperationLogger
from apps.users.models import User
from apps.users.serializers import UserSerializer
from utils.audit.audit_logger import AuditLogger

try:
    from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
    from rest_framework_simplejwt.tokens import Token
    HAS_TOKEN_BLACKLIST = True
except ImportError:
    HAS_TOKEN_BLACKLIST = False



class UserCommand:
    """Handle CRUD operations for User"""
    
    @staticmethod
    def _blacklist_user_tokens(user):
        """
        Blacklist all active tokens for a user.
        
        Args:
            user: User object
        """
        if not HAS_TOKEN_BLACKLIST:
            return
        
        try:
            from rest_framework_simplejwt.models import OutstandingToken
            
            # Get all outstanding tokens for this user
            outstanding_tokens = OutstandingToken.objects.filter(user=user)
            
            for token in outstanding_tokens:
                BlacklistedToken.objects.get_or_create(token=token)
            
            OperationLogger("UserCommand._blacklist_user_tokens", user_id=user.id).success(
                f"Blacklisted {outstanding_tokens.count()} tokens for user {user.id}"
            )
        except Exception as e:
            OperationLogger("UserCommand._blacklist_user_tokens", user_id=user.id).fail(
                f"Error blacklisting tokens: {str(e)}"
            )
    
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
            AuditLogger.log_failure(
                'CREATE',
                'User',
                performed_by=request.user if request else None,
                description=f"Failed to create user {username} - Missing required fields"
            )
            return BaseResultWithData(
                message="username, first_name, last_name, password, and groups are required",
                status_code=HTTPStatus.BAD_REQUEST
            )
        
        # Check if user already exists
        if User.objects.filter(username=username, is_deleted=False).exists():
            op.fail(f"User {username} already exists")
            AuditLogger.log_failure(
                'CREATE',
                'User',
                performed_by=request.user if request else None,
                description=f"Failed to create user {username} - User already exists"
            )
            return BaseResultWithData(
                message="Username already exists",
                status_code=HTTPStatus.BAD_REQUEST
            )
        
        # Check email only if provided
        if email and User.objects.filter(email=email, is_deleted=False).exists():
            op.fail(f"Email {email} already exists")
            AuditLogger.log_failure(
                'CREATE',
                'User',
                performed_by=request.user if request else None,
                description=f"Failed to create user {username} - Email {email} already exists"
            )
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
            
            # Log audit
            AuditLogger.log_create(
                entity='User',
                target_user=user,
                performed_by=request.user if request else None,
                description=f"Created user {username} ({first_name} {last_name}) with groups",
                metadata={'groups': [g.name for g in groups]}
            )
            
            return BaseResultWithData(
                message="User created successfully",
                data=UserSerializer(user).data,
                status_code=HTTPStatus.CREATED
            )


    @staticmethod
    def ChangePassword(user_id, new_password, performed_by=None):
        """
        Change user password.
        
        Args:
            user_id (int): User ID (required)
            new_password (str): New password (required)
            performed_by (User): User performing the action (optional)
            
        Returns:
            BaseResultWithData: Result with success message
        """
        op = OperationLogger(
            "ChangeUserPasswordCommand.ChangePassword",
            user_id=user_id
        )
        op.start()
        
        # Validate required fields
        if not all([user_id, new_password]):
            op.fail("Missing required fields: user_id, new_password")
            AuditLogger.log_failure(
                'CHANGE_PASSWORD',
                'User',
                performed_by=performed_by,
                description=f"Failed to change password for user {user_id} - Missing required fields"
            )
            return BaseResultWithData(
                message="user_id and new_password are required",
                status_code=HTTPStatus.BAD_REQUEST
            )
        
        try:
            user = User.objects.get(id=user_id, is_deleted=False)
            
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
            op.fail(f"User with ID {user_id} does not exist")
            AuditLogger.log_failure(
                'CHANGE_PASSWORD',
                'User',
                performed_by=performed_by,
                description=f"Failed to change password for user {user_id} - User not found"
            )
            return BaseResultWithData(
                message="User does not exist",
                status_code=HTTPStatus.NOT_FOUND
            )
            
    @staticmethod
    def Update(user_id, username=None, first_name=None, last_name=None, email=None, is_active=None, groups=None, performed_by=None):
        """
        Update user information (partial updates supported).
        
        Args:
            user_id (int): User ID (required)
            username (str): Username (optional)
            first_name (str): First name (optional)
            last_name (str): Last name (optional)
            email (str): Email address (optional)
            is_active (bool): Active status (optional)
            groups (list): List of Group objects (optional)
            performed_by (User): User performing the update (optional)
            
        Returns:
            BaseResultWithData: Result with updated user data
        """
        op = OperationLogger(
            "UserCommand.Update",
            user_id=user_id
        )
        op.start()
        
        try:
            user = User.objects.get(id=user_id, is_deleted=False)
            old_values = {}
            new_values = {}
            
            # Check for duplicate username if being updated
            if username is not None and username != user.username:
                if User.objects.filter(username=username, is_deleted=False).exists():
                    op.fail(f"Username {username} already exists")
                    AuditLogger.log_failure(
                        'UPDATE',
                        'User',
                        target_user=user,
                        performed_by=performed_by,
                        description=f"Failed to update user {user_id} - Username {username} already exists"
                    )
                    return BaseResultWithData(
                        message="Username already exists",
                        status_code=HTTPStatus.BAD_REQUEST
                    )
                old_values['username'] = user.username
                new_values['username'] = username
                user.username = username
            
            # Check for duplicate email if being updated
            if email is not None and email != user.email:
                if User.objects.filter(email=email, is_deleted=False).exists():
                    op.fail(f"Email {email} already exists")
                    AuditLogger.log_failure(
                        'UPDATE',
                        'User',
                        target_user=user,
                        performed_by=performed_by,
                        description=f"Failed to update user {user_id} - Email {email} already exists"
                    )
                    return BaseResultWithData(
                        message="Email already exists",
                        status_code=HTTPStatus.BAD_REQUEST
                    )
                old_values['email'] = user.email
                new_values['email'] = email
                user.email = email
            
            # Update other fields if provided
            if first_name is not None:
                old_values['first_name'] = user.first_name
                new_values['first_name'] = first_name
                user.first_name = first_name
            if last_name is not None:
                old_values['last_name'] = user.last_name
                new_values['last_name'] = last_name
                user.last_name = last_name
            if is_active is not None:
                old_values['is_active'] = user.is_active
                new_values['is_active'] = is_active
                user.is_active = is_active
                # Blacklist all tokens if user is being deactivated
                if is_active is False and HAS_TOKEN_BLACKLIST:
                    UserCommand._blacklist_user_tokens(user)
            
            with transaction.atomic():
                user.save()
                
                # Update groups if provided
                old_groups = list(user.groups.values_list('name', flat=True))
                if groups is not None:
                    user.groups.set(groups)
                    new_groups = list(user.groups.values_list('name', flat=True))
                    old_values['groups'] = old_groups
                    new_values['groups'] = new_groups
            
            op.success(f"User {user_id} updated successfully")
            
            # Log audit
            if old_values:
                AuditLogger.log_update(
                    entity='User',
                    target_user=user,
                    performed_by=performed_by,
                    description=f"Updated user {user_id} ({user.username})",
                    old_values=old_values,
                    new_values=new_values
                )
            
            return BaseResultWithData(
                message="User updated successfully",
                data=UserSerializer(user).data,
                status_code=HTTPStatus.OK
            )
        except User.DoesNotExist:
            op.fail("User not found")
            AuditLogger.log_failure(
                'UPDATE',
                'User',
                performed_by=performed_by,
                description=f"Failed to update user {user_id} - User not found"
            )
            return BaseResultWithData(
                message="User not found",
                status_code=HTTPStatus.NOT_FOUND
            )
    
    @staticmethod
    def ToggleDelete(user_id, performed_by=None):
        """
        Toggle user delete status (is_deleted true/false).
        
        Args:
            user_id (int): User ID
            performed_by (User): User performing the action
            
        Returns:
            BaseResultWithData: Result of toggle operation
        """
        op = OperationLogger(
            "UserCommand.ToggleDelete",
            user_id=user_id
        )
        op.start()
        
        try:
            user = User.objects.get(id=user_id)
            
            # Toggle is_deleted status
            user.is_deleted = not user.is_deleted
            user.save()
            
            status_text = "deleted" if user.is_deleted else "restored"
            op.success(f"User {user_id} {status_text}")
            
            # Log audit
            AuditLogger.log_toggle_delete(
                user=user,
                performed_by=performed_by,
                is_deleted=user.is_deleted,
                description=f"User {user.username} {status_text}"
            )
            
            return BaseResultWithData(
                message=f"User {status_text} successfully",
                status_code=HTTPStatus.OK
            )
        except User.DoesNotExist:
            op.fail("User not found")
            AuditLogger.log_failure(
                'TOGGLE_DELETE',
                'User',
                performed_by=performed_by,
                description=f"Failed to toggle delete for user {user_id} - User not found"
            )
            return BaseResultWithData(
                message="User not found",
                status_code=HTTPStatus.NOT_FOUND
            )