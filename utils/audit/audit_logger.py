from apps.administrator.models import AuditLog
from django.contrib.auth import get_user_model

User = get_user_model()


class AuditLogger:
    """Generic utility class for logging audit events"""
    
    @staticmethod
    def log(
        action,
        entity,
        status='SUCCESS',
        performed_by=None,
        target_user=None,
        description=None,
        old_values=None,
        new_values=None,
        metadata=None
    ):
        """
        Create an audit log entry.
        
        Args:
            action (str): Action type (CREATE, READ, UPDATE, DELETE, LOGIN, LOGOUT, CHANGE_PASSWORD, TOGGLE_DELETE)
            entity (str): Entity being acted upon (e.g., 'User', 'Group')
            status (str): Status of the action (SUCCESS, FAILED, PENDING)
            performed_by (User): User who performed the action
            target_user (User): User affected by the action
            description (str): Human-readable description
            old_values (dict): Previous values for updates
            new_values (dict): New values for updates
            metadata (dict): Additional metadata
            
        Returns:
            AuditLog: Created audit log entry
        """
        return AuditLog.objects.create(
            action=action,
            entity=entity,
            status=status,
            performed_by=performed_by,
            target_user=target_user,
            description=description or f"{action} {entity}",
            old_values=old_values,
            new_values=new_values,
            metadata=metadata
        )
    
    @staticmethod
    def log_create(entity, target_user=None, performed_by=None, description=None, metadata=None):
        """Log a CREATE action"""
        return AuditLogger.log(
            action='CREATE',
            entity=entity,
            status='SUCCESS',
            target_user=target_user,
            performed_by=performed_by,
            description=description,
            metadata=metadata
        )
    
    @staticmethod
    def log_read(entity, target_user=None, performed_by=None, description=None, metadata=None):
        """Log a READ action"""
        return AuditLogger.log(
            action='READ',
            entity=entity,
            status='SUCCESS',
            target_user=target_user,
            performed_by=performed_by,
            description=description,
            metadata=metadata
        )
    
    @staticmethod
    def log_update(entity, target_user=None, performed_by=None, description=None, old_values=None, new_values=None, metadata=None):
        """Log an UPDATE action"""
        return AuditLogger.log(
            action='UPDATE',
            entity=entity,
            status='SUCCESS',
            target_user=target_user,
            performed_by=performed_by,
            description=description,
            old_values=old_values,
            new_values=new_values,
            metadata=metadata
        )
    
    @staticmethod
    def log_delete(entity, target_user=None, performed_by=None, description=None, metadata=None):
        """Log a DELETE action"""
        return AuditLogger.log(
            action='DELETE',
            entity=entity,
            status='SUCCESS',
            target_user=target_user,
            performed_by=performed_by,
            description=description,
            metadata=metadata
        )
    
    @staticmethod
    def log_login(user, description=None, metadata=None):
        """Log a LOGIN action"""
        return AuditLogger.log(
            action='LOGIN',
            entity='User',
            status='SUCCESS',
            performed_by=user,
            target_user=user,
            description=description or f"User {user.username} logged in",
            metadata=metadata
        )
    
    @staticmethod
    def log_logout(user, description=None, metadata=None):
        """Log a LOGOUT action"""
        return AuditLogger.log(
            action='LOGOUT',
            entity='User',
            status='SUCCESS',
            performed_by=user,
            target_user=user,
            description=description or f"User {user.username} logged out",
            metadata=metadata
        )
    
    @staticmethod
    def log_password_change(user, performed_by=None, description=None, metadata=None):
        """Log a CHANGE_PASSWORD action"""
        return AuditLogger.log(
            action='CHANGE_PASSWORD',
            entity='User',
            status='SUCCESS',
            target_user=user,
            performed_by=performed_by or user,
            description=description or f"Password changed for user {user.username}",
            metadata=metadata
        )
    
    @staticmethod
    def log_toggle_delete(user, performed_by=None, is_deleted=False, description=None, metadata=None):
        """Log a TOGGLE_DELETE action"""
        status_text = "deleted" if is_deleted else "restored"
        return AuditLogger.log(
            action='TOGGLE_DELETE',
            entity='User',
            status='SUCCESS',
            target_user=user,
            performed_by=performed_by,
            description=description or f"User {user.username} {status_text}",
            new_values={'is_deleted': is_deleted},
            metadata=metadata
        )
    
    @staticmethod
    def log_failure(action, entity, performed_by=None, target_user=None, description=None, metadata=None):
        """Log a failed action"""
        return AuditLogger.log(
            action=action,
            entity=entity,
            status='FAILED',
            performed_by=performed_by,
            target_user=target_user,
            description=description,
            metadata=metadata
        )
