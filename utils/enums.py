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


class RoomStatus(Enum):
    """Room status types"""
    AVAILABLE = "AVAILABLE"
    OCCUPIED = "OCCUPIED"
    DIRTY = "DIRTY"
    MAINTENANCE = "MAINTENANCE"
    
    @classmethod
    def choices(cls):
        """Return choices for Django model field"""
        return [(status.value, status.value.title()) for status in cls]


class BookingStatus(Enum):
    """Booking status types"""
    RESERVED = "RESERVED"
    CHECKED_IN = "CHECKED_IN"
    CHECKED_OUT = "CHECKED_OUT"
    CANCELLED = "CANCELLED"
    NO_SHOW = "NO_SHOW"
    
    @classmethod
    def choices(cls):
        """Return choices for Django model field"""
        return [(status.value, status.value.replace('_', ' ').title()) for status in cls]


class PaymentMethod(Enum):
    """Payment method types"""
    CASH = "CASH"
    CARD = "CARD"
    TRANSFER = "TRANSFER"
    
    @classmethod
    def choices(cls):
        """Return choices for Django model field"""
        return [(method.value, method.value.title()) for method in cls]


class PaymentStatus(Enum):
    """Payment status types"""
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"
    
    @classmethod
    def choices(cls):
        """Return choices for Django model field"""
        return [(status.value, status.value.title()) for status in cls]