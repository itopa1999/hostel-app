from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone
from utils.base_model import BaseModel
from utils.Middlewares.threadlocals import get_current_user



@receiver(pre_save)
def auto_fill_audit_fields(sender, instance, **kwargs):
    """Handle pre-save audit fields - do NOT access ManyToMany relationships here"""
    # Only for models inheriting from BaseModel
    if not issubclass(sender, BaseModel):
        return

    user = get_current_user()
    action_by = getattr(user, "username", None) or getattr(user, "email", None) or "System"

    if instance._state.adding:
        if not instance.created_by:
            instance.created_by = action_by
    else:
        instance.modified_by = action_by

    if instance.is_deleted and not instance.deleted_at:
        instance.deleted_at = timezone.now()
        instance.deleted_by = action_by