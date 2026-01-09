from celery import shared_task
from apps.administrator.models import AuditLog
from utils.log_helpers import OperationLogger


@shared_task(bind=True, max_retries=3)
def log_audit_event(self, action, entity, status, description=None, 
                    performed_by_id=None, target_user_id=None, 
                    old_values=None, new_values=None, metadata=None):
    """
    Log audit events asynchronously in background
    
    Args:
        action: Action type (CREATE, UPDATE, DELETE, etc.)
        entity: Entity name (User, Hotel, Booking, etc.)
        status: Status (SUCCESS, FAILURE, PENDING)
        description: Human-readable description
        performed_by_id: ID of user who performed action
        target_user_id: ID of user affected by action
        old_values: Previous values for updates
        new_values: New values for updates
        metadata: Additional metadata
    
    Retries 3 times on failure
    """
    op = OperationLogger(
        "log_audit_event",
        action=action,
        entity=entity,
        status=status
    )
    op.start()
    
    try:
        audit_log = AuditLog.objects.create(
            action=action,
            entity=entity,
            status=status,
            description=description,
            performed_by_id=performed_by_id,
            target_user_id=target_user_id,
            old_values=old_values,
            new_values=new_values,
            metadata=metadata,
        )
        op.success(f"Audit logged: {action} on {entity} (ID: {audit_log.id})")
        return f"Audit event logged successfully - ID: {audit_log.id}"
    except Exception as exc:
        op.fail(f"Failed to log audit event", exc=exc)
        raise self.retry(exc=exc, countdown=30)
