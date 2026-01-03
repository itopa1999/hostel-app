from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

from utils.base_model import BaseModel
from utils.enums import AuditAction, AuditStatus

User = get_user_model()


class AuditLog(BaseModel):
    """Log all system actions and commands"""
    
    # Core fields
    action = models.CharField(max_length=20, choices=AuditAction.choices())
    entity = models.CharField(max_length=100, help_text="Entity being acted upon (e.g., User, Group)")
    status = models.CharField(max_length=20, choices=AuditStatus.choices(), default=AuditStatus.PENDING.value)
    
    # User performing the action
    performed_by = models.ForeignKey(
        User, 
        on_delete=models.PROTECT, 
        related_name='audit_logs_created',
        null=True,
        blank=True,
        help_text="User who performed the action"
    )
    
    # Target user/entity
    target_user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='audit_logs_targeted',
        null=True,
        blank=True,
        help_text="User who was affected by the action"
    )
    
    # Details
    description = models.TextField(blank=True, help_text="Human-readable description of the action")
    old_values = models.JSONField(null=True, blank=True, help_text="Previous values (for updates)")
    new_values = models.JSONField(null=True, blank=True, help_text="New values (for updates)")
    metadata = models.JSONField(null=True, blank=True, help_text="Additional metadata")

    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['action', '-created_at']),
            models.Index(fields=['performed_by', '-created_at']),
            models.Index(fields=['target_user', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.action} - {self.entity} ({self.status}) - {self.created_at}"


