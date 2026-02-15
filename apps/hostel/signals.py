from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from apps.hostel.models import Hotel
from utils.cache_helper import GlobalCache
from utils.enums import CacheKeys


@receiver(post_save, sender=Hotel)
def invalidate_hotel_cache_on_save(sender, instance, created, **kwargs):
    """Invalidate hotel cache when a hotel is created or updated"""
    GlobalCache.delete(CacheKeys.HOTEL_FIRST.value)
    GlobalCache.delete(CacheKeys.HOTEL_ALL.value)
    # Also clear any hotel-related cache with prefix
    GlobalCache.delete_prefix("hotel:")


@receiver(post_delete, sender=Hotel)
def invalidate_hotel_cache_on_delete(sender, instance, **kwargs):
    """Invalidate hotel cache when a hotel is deleted"""
    GlobalCache.delete(CacheKeys.HOTEL_FIRST.value)
    GlobalCache.delete(CacheKeys.HOTEL_ALL.value)
    # Also clear any hotel-related cache with prefix
    GlobalCache.delete_prefix("hotel:")
