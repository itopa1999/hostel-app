from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth.models import Group
from apps.users.models import User
from utils.base_model import BaseModel
from utils.Middlewares.threadlocals import get_current_user
from utils.enums import GroupNames
from utils.cache_helper import GlobalCache
from utils.enums import CacheKeys


# Dynamic Group to ID prefix mapping based on enum
GROUP_ID_PREFIX = {
    GroupNames.ADMIN.value: 'ADM',
    GroupNames.MANAGER.value: 'MGR',
    GroupNames.STAFF.value: 'STA',
    GroupNames.USER.value: 'USR',
}


def generate_id_number(group_name):
    """Generate an incremental ID number based on group."""
    from apps.users.models import User
    
    prefix = GROUP_ID_PREFIX.get(group_name, 'USR')
    
    # Find the last user with this prefix
    last_user = User.objects.filter(
        id_number__startswith=f"{prefix}-ID-"
    ).order_by('-id_number').first()
    
    if last_user and last_user.id_number:
        try:
            last_number = int(last_user.id_number.split('-')[-1])
            next_number = last_number + 1
        except (ValueError, IndexError):
            next_number = 1
    else:
        next_number = 1
    
    # Format as 3-digit number with leading zeros
    return f"{prefix}-ID-{next_number:03d}"



@receiver(post_save)
def auto_assign_user_id_number(sender, instance, created, **kwargs):
    """Auto-assign id_number for User model after creation based on groups"""
    # Only for User model
    if sender.__name__ != 'User':
        return
    
    # Only on creation
    if not created:
        return
    
    # Only if id_number not already assigned
    if instance.id_number:
        return
    
    # Auto-assign Admin group to superusers if no groups
    if instance.is_superuser and not instance.groups.exists():
        from django.contrib.auth.models import Group
        admin_group, _ = Group.objects.get_or_create(name=GroupNames.ADMIN.value)
        instance.groups.add(admin_group)
    
    # Get the primary group
    groups = instance.groups.all()
    if groups.exists():
        group_name = groups.first().name
        instance.id_number = generate_id_number(group_name)
    else:
        # Default to User group if no group assigned
        instance.id_number = generate_id_number('User')
    
    # Save without triggering signals again
    instance.save(update_fields=['id_number'])


# User Cache Invalidation
@receiver(post_save, sender=User)
def invalidate_user_cache_on_save(sender, instance, created, **kwargs):
    """Invalidate user cache when a user is created or updated"""
    GlobalCache.delete(CacheKeys.USER_ALL.value)
    GlobalCache.delete(CacheKeys.format(CacheKeys.USER_ID, user_id=instance.id))
    GlobalCache.delete_prefix("user:")


@receiver(post_delete, sender=User)
def invalidate_user_cache_on_delete(sender, instance, **kwargs):
    """Invalidate user cache when a user is deleted (soft delete)"""
    GlobalCache.delete(CacheKeys.USER_ALL.value)
    GlobalCache.delete(CacheKeys.format(CacheKeys.USER_ID, user_id=instance.id))
    GlobalCache.delete_prefix("user:")


# Group Cache Invalidation
@receiver(post_save, sender=Group)
def invalidate_group_cache_on_save(sender, instance, created, **kwargs):
    """Invalidate group cache when a group is created or updated"""
    GlobalCache.delete(CacheKeys.GROUP_ALL.value)
    GlobalCache.delete_prefix("group:")
    # Also invalidate user cache since groups affect user data
    GlobalCache.delete(CacheKeys.USER_ALL.value)
    GlobalCache.delete_prefix("user:")


@receiver(post_delete, sender=Group)
def invalidate_group_cache_on_delete(sender, instance, **kwargs):
    """Invalidate group cache when a group is deleted"""
    GlobalCache.delete(CacheKeys.GROUP_ALL.value)
    GlobalCache.delete_prefix("group:")
    # Also invalidate user cache
    GlobalCache.delete(CacheKeys.USER_ALL.value)
    GlobalCache.delete_prefix("user:")
      