from enum import Enum


class GroupNames(Enum):
    ADMIN = "Admin"
    MANAGER = "Manager"
    STAFF = "Staff"
    USER = "User"
    
    @classmethod
    def values(cls):
        """Return all enum values as a list"""
        return [group.value for group in cls]


class AuditAction(Enum):
    """Audit log action types"""
    CREATE = "CREATE"
    READ = "READ"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"
    CHANGE_PASSWORD = "CHANGE_PASSWORD"
    TOGGLE_DELETE = "TOGGLE_DELETE"
    
    @classmethod
    def choices(cls):
        """Return choices for Django model field"""
        return [(action.value, action.value.replace('_', ' ').title()) for action in cls]


class AuditStatus(Enum):
    """Audit log status types"""
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    PENDING = "PENDING"
    
    @classmethod
    def choices(cls):
        """Return choices for Django model field"""
        return [(status.value, status.value.title()) for status in cls]
