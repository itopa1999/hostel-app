from http import HTTPStatus
from django.db.models import Q
from django.db import transaction
from django.contrib.auth.models import Group
from utils.base_result import BaseResultWithData
from utils.log_helpers import OperationLogger
from apps.users.models import User
from apps.users.serializers import UserDetailSerializer
from utils.audit.audit_logger import AuditLogger


class UserCommand:
    """Handle CRUD operations for User"""
    
    @staticmethod
    def Create(data, performed_by=None):
        """
        Create a new user.
        
        Args:
            data (dict): User data (username, password, email, first_name, last_name, groups)
            performed_by (User): User performing the action
            
        Returns:
            BaseResultWithData: Result with created user data
        """
        op = OperationLogger("UserCommand.Create")
        op.start()
        
        # Validate required fields
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        if not username or not password:
            op.fail("Missing required fields: username and password")
            return BaseResultWithData(
                message="Username and password are required",
                status_code=HTTPStatus.BAD_REQUEST
            )
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            op.fail(f"Username '{username}' already exists")
            return BaseResultWithData(
                message=f"Username '{username}' already exists",
                status_code=HTTPStatus.BAD_REQUEST
            )
        
        try:
            with transaction.atomic():
                # Create user
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=data.get('email', '').strip() or None,
                    first_name=data.get('first_name', '').strip(),
                    last_name=data.get('last_name', '').strip(),
                    is_active=data.get('is_active', True),
                    is_staff=data.get('is_staff', False)
                )
                
                # Assign groups if provided
                group_ids = data.get('groups', [])
                if group_ids:
                    groups = Group.objects.filter(id__in=group_ids)
                    user.groups.set(groups)
                else:
                    # Clear all groups if none provided
                    user.groups.clear()
                
                op.success(f"User {username} created successfully")
                
                AuditLogger.log_create(
                    'User',
                    performed_by=performed_by,
                    target_user=user,
                    metadata=f"User {username} created with groups: {', '.join(user.groups.values_list('name', flat=True)) or 'None'}"
                )
                
                serializer = UserDetailSerializer(user)
                return BaseResultWithData(
                    message="User created successfully",
                    data=serializer.data,
                    status_code=HTTPStatus.CREATED
                )
        except Exception as e:
            op.fail(f"Failed to create user: {str(e)}", exc=e)
            AuditLogger.log_failure(
                'CREATE_USER',
                'User',
                performed_by=performed_by,
                description=f"Failed to create user - {str(e)}"
            )
            return BaseResultWithData(
                message=str(e),
                status_code=HTTPStatus.BAD_REQUEST
            )
    
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
                    status_code=HTTPStatus.BAD_REQUEST
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
    
    @staticmethod
    def Update(user_id, email=None, first_name=None, last_name=None, performed_by=None):
        """
        Update user profile information (email, first_name, last_name).
        
        Args:
            user_id (int): User ID to update
            email (str): New email address (optional)
            first_name (str): New first name (optional)
            last_name (str): New last name (optional)
            performed_by (User): User performing the action
            
        Returns:
            BaseResultWithData: Result with updated user data
        """
        op = OperationLogger("UserCommand.Update", user_id=user_id)
        op.start()
        
        try:
            user = User.objects.get(id=user_id, is_deleted=False)
            
            # Store old values for audit log
            old_values = {}
            new_values = {}
            
            # Check for duplicate email if being updated
            if email is not None and email.strip() and email != user.email:
                email_stripped = email.strip()
                if User.objects.filter(email=email_stripped, is_deleted=False).exclude(id=user_id).exists():
                    op.fail(f"Email {email_stripped} already exists")
                    AuditLogger.log_failure(
                        'UPDATE',
                        'User',
                        target_user=user,
                        performed_by=performed_by,
                        description=f"Failed to update user {user_id} - Email {email_stripped} already exists"
                    )
                    return BaseResultWithData(
                        message="Email already exists",
                        status_code=HTTPStatus.BAD_REQUEST
                    )
                old_values['email'] = user.email
                new_values['email'] = email_stripped
                user.email = email_stripped
            
            # Update first_name if provided
            if first_name is not None:
                first_name_stripped = first_name.strip() if first_name else ""
                if first_name_stripped != user.first_name:
                    old_values['first_name'] = user.first_name
                    new_values['first_name'] = first_name_stripped
                    user.first_name = first_name_stripped
            
            # Update last_name if provided
            if last_name is not None:
                last_name_stripped = last_name.strip() if last_name else ""
                if last_name_stripped != user.last_name:
                    old_values['last_name'] = user.last_name
                    new_values['last_name'] = last_name_stripped
                    user.last_name = last_name_stripped
            
            # Only save if there were changes
            if old_values:
                user.save()
                op.success(f"User {user.username} profile updated successfully")
                
                AuditLogger.log_update(
                    entity='User',
                    target_user=user,
                    performed_by=performed_by,
                    description=f"Updated profile for user {user.username}",
                    old_values=old_values,
                    new_values=new_values
                )
            else:
                op.success(f"No changes made to user {user.username}")
            
            serializer = UserDetailSerializer(user)
            return BaseResultWithData(
                message="User profile updated successfully",
                data=serializer.data,
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
        except Exception as e:
            op.fail(f"Failed to update user: {str(e)}", exc=e)
            AuditLogger.log_failure(
                'UPDATE',
                'User',
                performed_by=performed_by,
                description=f"Failed to update user {user_id} - {str(e)}"
            )
            return BaseResultWithData(
                message=str(e),
                status_code=HTTPStatus.BAD_REQUEST
            )
    
    @staticmethod
    def ToggleDelete(user_id, performed_by=None):
        """
        Soft delete or restore a user (toggle is_deleted flag).
        
        Args:
            user_id (int): User ID to delete/restore
            performed_by (User): User performing the action
            
        Returns:
            BaseResultWithData: Result with updated user data
        """
        op = OperationLogger("UserCommand.ToggleDelete", user_id=user_id)
        op.start()
        
        try:
            user = User.objects.get(id=user_id)
            
            old_is_deleted = user.is_deleted
            user.is_deleted = not user.is_deleted
            user.save()
            
            action = "deleted" if user.is_deleted else "restored"
            op.success(f"User {user_id} {action} successfully")
            
            AuditLogger.log_update(
                'User',
                performed_by=performed_by,
                target_user=user,
                old_values={"is_deleted": old_is_deleted},
                new_values={"is_deleted": user.is_deleted},
                description=f"User {user.username} {action}"
            )
            
            serializer = UserDetailSerializer(user)
            return BaseResultWithData(
                message=f"User {action} successfully",
                data=serializer.data,
                status_code=HTTPStatus.OK
            )
        except User.DoesNotExist:
            op.fail(f"User with id {user_id} not found")
            AuditLogger.log_failure(
                'DELETE_USER',
                'User',
                performed_by=performed_by,
                description=f"Failed to delete user {user_id} - User not found"
            )
            return BaseResultWithData(
                message="User not found",
                status_code=HTTPStatus.NOT_FOUND
            )
        except Exception as e:
            op.fail(f"Failed to toggle delete user: {str(e)}", exc=e)
            AuditLogger.log_failure(
                'DELETE_USER',
                'User',
                performed_by=performed_by,
                description=f"Failed to delete user {user_id} - {str(e)}"
            )
            return BaseResultWithData(
                message=str(e),
                status_code=HTTPStatus.BAD_REQUEST
            )
    
    @staticmethod
    def UpdateGroups(user_id, group_ids, password=None, performed_by=None):
        """
        Update user's groups and optionally password.
        
        Args:
            user_id (int): User ID
            group_ids (list): List of group IDs to assign to user
            password (str): Optional new password (min 6 chars)
            performed_by (User): User performing the action
            
        Returns:
            BaseResultWithData: Result with updated user data
        """
        if not group_ids:
            return BaseResultWithData(
                message="group_ids is required",
                status_code=HTTPStatus.BAD_REQUEST
            )
        
        # Validate password if provided
        if password:
            password = password.strip()
            if len(password) < 6:
                return BaseResultWithData(
                    message="Password must be at least 6 characters long",
                    status_code=HTTPStatus.BAD_REQUEST
                )
        
        op = OperationLogger("UserCommand.UpdateGroups", user_id=user_id)
        op.start()
        
        try:
            user = User.objects.get(id=user_id)
            
            # Validate group IDs exist
            groups = Group.objects.filter(id__in=group_ids)
            if groups.count() != len(group_ids):
                op.fail(f"One or more group IDs are invalid")
                return BaseResultWithData(
                    message="One or more group IDs are invalid",
                    status_code=HTTPStatus.BAD_REQUEST
                )
            
            # Get old values for audit
            old_groups = list(user.groups.values_list('name', flat=True))
            changes = {}
            
            # Update groups
            user.groups.set(groups)
            
            # Update password if provided
            if password:
                user.set_password(password)
                changes['password'] = 'Changed'
            
            user.save()
            op.success(f"Groups updated for user {user_id}")
            
            # Get new groups for audit
            new_groups = list(user.groups.values_list('name', flat=True))
            changes['groups'] = new_groups
            
            audit_description = f"Groups updated for user {user.username}: {', '.join(new_groups)}"
            if password:
                audit_description += "; Password changed"
            
            AuditLogger.log_update(
                'User',
                performed_by=performed_by,
                target_user=user,
                old_values={"groups": old_groups},
                new_values=changes,
                description=audit_description
            )
            
            serializer = UserDetailSerializer(user)
            return BaseResultWithData(
                message="Groups updated successfully",
                data=serializer.data,
                status_code=HTTPStatus.OK
            )
        except User.DoesNotExist:
            op.fail(f"User with id {user_id} not found")
            return BaseResultWithData(
                message="User not found",
                status_code=HTTPStatus.NOT_FOUND
            )
        except Exception as e:
            op.fail(f"Failed to update groups: {str(e)}", exc=e)
            return BaseResultWithData(
                message=str(e),
                status_code=HTTPStatus.BAD_REQUEST
            )



