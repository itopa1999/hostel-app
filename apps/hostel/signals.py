from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from apps.hostel.models import Hotel, Floor, Room, RoomType, Setting, Booking, Invoice, Payment, GuestProfile
from utils.cache_helper import GlobalCache
from utils.enums import CacheKeys


# Hotel Cache Invalidation
@receiver(post_save, sender=Hotel)
def invalidate_hotel_cache_on_save(sender, instance, created, **kwargs):
    """Invalidate hotel cache when a hotel is created or updated"""
    GlobalCache.delete(CacheKeys.HOTEL_FIRST.value)
    GlobalCache.delete(CacheKeys.HOTEL_ALL.value)
    GlobalCache.delete_prefix("hotel:")


@receiver(post_delete, sender=Hotel)
def invalidate_hotel_cache_on_delete(sender, instance, **kwargs):
    """Invalidate hotel cache when a hotel is deleted"""
    GlobalCache.delete(CacheKeys.HOTEL_FIRST.value)
    GlobalCache.delete(CacheKeys.HOTEL_ALL.value)
    GlobalCache.delete_prefix("hotel:")


# Setting Cache Invalidation
@receiver(post_save, sender=Setting)
def invalidate_setting_cache_on_save(sender, instance, created, **kwargs):
    """Invalidate setting cache when a setting is created or updated"""
    GlobalCache.delete(CacheKeys.SETTINGS_GENERAL.value)
    GlobalCache.delete(CacheKeys.SETTINGS_ALL.value)
    GlobalCache.delete_prefix("settings:")


@receiver(post_delete, sender=Setting)
def invalidate_setting_cache_on_delete(sender, instance, **kwargs):
    """Invalidate setting cache when a setting is deleted"""
    GlobalCache.delete(CacheKeys.SETTINGS_GENERAL.value)
    GlobalCache.delete(CacheKeys.SETTINGS_ALL.value)
    GlobalCache.delete_prefix("settings:")


# Floor Cache Invalidation
@receiver(post_save, sender=Floor)
def invalidate_floor_cache_on_save(sender, instance, created, **kwargs):
    """Invalidate floor cache when a floor is created or updated"""
    GlobalCache.delete(CacheKeys.FLOOR_ALL.value)
    GlobalCache.delete(CacheKeys.format(CacheKeys.FLOOR_ID, floor_id=instance.id))
    GlobalCache.delete_prefix("floor:")
    # Also invalidate dashboard cache since it depends on floor data
    GlobalCache.delete(CacheKeys.DASHBOARD_STATS.value)
    GlobalCache.delete_prefix("dashboard:")


@receiver(post_delete, sender=Floor)
def invalidate_floor_cache_on_delete(sender, instance, **kwargs):
    """Invalidate floor cache when a floor is deleted (soft delete)"""
    GlobalCache.delete(CacheKeys.FLOOR_ALL.value)
    GlobalCache.delete(CacheKeys.format(CacheKeys.FLOOR_ID, floor_id=instance.id))
    GlobalCache.delete_prefix("floor:")
    GlobalCache.delete(CacheKeys.DASHBOARD_STATS.value)
    GlobalCache.delete_prefix("dashboard:")


# Room Cache Invalidation
@receiver(post_save, sender=Room)
def invalidate_room_cache_on_save(sender, instance, created, **kwargs):
    """Invalidate room cache when a room is created or updated"""
    GlobalCache.delete(CacheKeys.ROOM_ALL.value)
    GlobalCache.delete(CacheKeys.format(CacheKeys.ROOM_ID, room_id=instance.id))
    GlobalCache.delete(CacheKeys.ROOM_AVAILABLE.value)
    GlobalCache.delete_prefix("room:")
    # Invalidate floor cache since it has room counts
    GlobalCache.delete(CacheKeys.FLOOR_ALL.value)
    GlobalCache.delete_prefix("floor:")
    # Invalidate dashboard cache
    GlobalCache.delete(CacheKeys.DASHBOARD_STATS.value)
    GlobalCache.delete_prefix("dashboard:")


@receiver(post_delete, sender=Room)
def invalidate_room_cache_on_delete(sender, instance, **kwargs):
    """Invalidate room cache when a room is deleted (soft delete)"""
    GlobalCache.delete(CacheKeys.ROOM_ALL.value)
    GlobalCache.delete(CacheKeys.format(CacheKeys.ROOM_ID, room_id=instance.id))
    GlobalCache.delete(CacheKeys.ROOM_AVAILABLE.value)
    GlobalCache.delete_prefix("room:")
    GlobalCache.delete(CacheKeys.FLOOR_ALL.value)
    GlobalCache.delete_prefix("floor:")
    GlobalCache.delete(CacheKeys.DASHBOARD_STATS.value)
    GlobalCache.delete_prefix("dashboard:")


# RoomType Cache Invalidation
@receiver(post_save, sender=RoomType)
def invalidate_room_type_cache_on_save(sender, instance, created, **kwargs):
    """Invalidate room type cache when a room type is created or updated"""
    GlobalCache.delete(CacheKeys.ROOM_TYPE_ALL.value)
    GlobalCache.delete(CacheKeys.format(CacheKeys.ROOM_TYPE_ID, room_type_id=instance.id))
    GlobalCache.delete_prefix("room_type:")


@receiver(post_delete, sender=RoomType)
def invalidate_room_type_cache_on_delete(sender, instance, **kwargs):
    """Invalidate room type cache when a room type is deleted (soft delete)"""
    GlobalCache.delete(CacheKeys.ROOM_TYPE_ALL.value)
    GlobalCache.delete(CacheKeys.format(CacheKeys.ROOM_TYPE_ID, room_type_id=instance.id))
    GlobalCache.delete_prefix("room_type:")


# Booking Cache Invalidation
@receiver(post_save, sender=Booking)
def invalidate_booking_cache_on_save(sender, instance, created, **kwargs):
    """Invalidate booking cache when a booking is created or updated"""
    GlobalCache.delete(CacheKeys.BOOKING_ALL.value)
    GlobalCache.delete(CacheKeys.format(CacheKeys.BOOKING_ID, booking_id=instance.id))
    GlobalCache.delete_prefix("booking:")
    # Invalidate dashboard cache
    GlobalCache.delete(CacheKeys.DASHBOARD_STATS.value)
    GlobalCache.delete_prefix("dashboard:")


@receiver(post_delete, sender=Booking)
def invalidate_booking_cache_on_delete(sender, instance, **kwargs):
    """Invalidate booking cache when a booking is deleted (soft delete)"""
    GlobalCache.delete(CacheKeys.BOOKING_ALL.value)
    GlobalCache.delete(CacheKeys.format(CacheKeys.BOOKING_ID, booking_id=instance.id))
    GlobalCache.delete_prefix("booking:")
    GlobalCache.delete(CacheKeys.DASHBOARD_STATS.value)
    GlobalCache.delete_prefix("dashboard:")


# Invoice Cache Invalidation
@receiver(post_save, sender=Invoice)
def invalidate_invoice_cache_on_save(sender, instance, created, **kwargs):
    """Invalidate invoice cache when an invoice is created or updated"""
    GlobalCache.delete(CacheKeys.INVOICE_ALL.value)
    GlobalCache.delete(CacheKeys.format(CacheKeys.INVOICE_ID, invoice_id=instance.id))
    GlobalCache.delete_prefix("invoice:")
    # Invalidate dashboard cache
    GlobalCache.delete(CacheKeys.DASHBOARD_STATS.value)
    GlobalCache.delete_prefix("dashboard:")


@receiver(post_delete, sender=Invoice)
def invalidate_invoice_cache_on_delete(sender, instance, **kwargs):
    """Invalidate invoice cache when an invoice is deleted (soft delete)"""
    GlobalCache.delete(CacheKeys.INVOICE_ALL.value)
    GlobalCache.delete(CacheKeys.format(CacheKeys.INVOICE_ID, invoice_id=instance.id))
    GlobalCache.delete_prefix("invoice:")
    GlobalCache.delete(CacheKeys.DASHBOARD_STATS.value)
    GlobalCache.delete_prefix("dashboard:")


# Payment Cache Invalidation
@receiver(post_save, sender=Payment)
def invalidate_payment_cache_on_save(sender, instance, created, **kwargs):
    """Invalidate payment cache when a payment is created or updated"""
    GlobalCache.delete(CacheKeys.PAYMENT_ALL.value)
    GlobalCache.delete(CacheKeys.format(CacheKeys.PAYMENT_ID, payment_id=instance.id))
    GlobalCache.delete_prefix("payment:")
    # Invalidate dashboard cache
    GlobalCache.delete(CacheKeys.DASHBOARD_STATS.value)
    GlobalCache.delete_prefix("dashboard:")


@receiver(post_delete, sender=Payment)
def invalidate_payment_cache_on_delete(sender, instance, **kwargs):
    """Invalidate payment cache when a payment is deleted (soft delete)"""
    GlobalCache.delete(CacheKeys.PAYMENT_ALL.value)
    GlobalCache.delete(CacheKeys.format(CacheKeys.PAYMENT_ID, payment_id=instance.id))
    GlobalCache.delete_prefix("payment:")
    GlobalCache.delete(CacheKeys.DASHBOARD_STATS.value)
    GlobalCache.delete_prefix("dashboard:")


# GuestProfile Cache Invalidation
@receiver(post_save, sender=GuestProfile)
def invalidate_guest_cache_on_save(sender, instance, created, **kwargs):
    """Invalidate guest cache when a guest is created or updated"""
    GlobalCache.delete(CacheKeys.GUEST_ALL.value)
    GlobalCache.delete(CacheKeys.format(CacheKeys.GUEST_ID, guest_id=instance.id))
    GlobalCache.delete_prefix("guest:")
    # Invalidate dashboard cache
    GlobalCache.delete(CacheKeys.DASHBOARD_STATS.value)
    GlobalCache.delete_prefix("dashboard:")


@receiver(post_delete, sender=GuestProfile)
def invalidate_guest_cache_on_delete(sender, instance, **kwargs):
    """Invalidate guest cache when a guest is deleted (soft delete)"""
    GlobalCache.delete(CacheKeys.GUEST_ALL.value)
    GlobalCache.delete(CacheKeys.format(CacheKeys.GUEST_ID, guest_id=instance.id))
    GlobalCache.delete_prefix("guest:")
    GlobalCache.delete(CacheKeys.DASHBOARD_STATS.value)
    GlobalCache.delete_prefix("dashboard:")
