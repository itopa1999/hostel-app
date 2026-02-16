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
    
    
class CacheKeys(Enum):
    """
    Centralized cache key names for consistency across the project.
    Always use CacheKeys.KEY_NAME.value when accessing cache.
    """
    # Hotel Cache
    HOTEL_FIRST = "hotel:first"
    HOTEL_ALL = "hotel:all"
    HOTEL_ID = "hotel:id:{hotel_id}"
    
    # Settings Cache
    SETTINGS_GENERAL = "settings:general"
    SETTINGS_ALL = "settings:all"
    
    # Room Cache
    ROOM_ALL = "room:all"
    ROOM_ID = "room:id:{room_id}"
    ROOM_AVAILABLE = "room:available"
    
    # Floor Cache
    FLOOR_ALL = "floor:all"
    FLOOR_ID = "floor:id:{floor_id}"
    
    # Room Type Cache
    ROOM_TYPE_ALL = "room_type:all"
    ROOM_TYPE_ID = "room_type:id:{room_type_id}"
    
    # Booking Cache
    BOOKING_ALL = "booking:all"
    BOOKING_ID = "booking:id:{booking_id}"
    
    # Invoice Cache
    INVOICE_ALL = "invoice:all"
    INVOICE_ID = "invoice:id:{invoice_id}"
    
    # Payment Cache
    PAYMENT_ALL = "payment:all"
    PAYMENT_ID = "payment:id:{payment_id}"
    
    # Guest Profile Cache
    GUEST_ALL = "guest:all"
    GUEST_ID = "guest:id:{guest_id}"
    
    # Dashboard Cache
    DASHBOARD_STATS = "dashboard:stats"
    DASHBOARD_OCCUPANCY = "dashboard:occupancy"
    
    # User Cache
    USER_PROFILE = "user:profile:{user_id}"
    USER_ALL = "user:all"
    USER_ID = "user:id:{user_id}"
    
    # Group Cache
    GROUP_ALL = "group:all"

    @classmethod
    def format(cls, key, **kwargs):
        """
        Helper method to fill in placeholders for formatted keys.
        Example:
            CacheKeys.format(CacheKeys.USER_PROFILE, user_id=5)
        """
        return key.value.format(**kwargs)
    
