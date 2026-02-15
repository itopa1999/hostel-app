import csv
import os
from datetime import datetime, timedelta
from celery import shared_task
from django.apps import apps
from django.db.models import Q
from django.utils import timezone

from apps.administrator.models import AuditLog, Backup
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


@shared_task(bind=True, max_retries=3)
def generate_backup_csv(self, backup_id):
    """
    Generate backup CSV file for all records in a date range
    
    Args:
        backup_id: ID of the Backup record to process
    
    Retries 3 times on failure
    """
    op = OperationLogger("generate_backup_csv", backup_id=backup_id)
    op.start()
    
    try:
        # Fetch the backup record
        backup = Backup.objects.get(id=backup_id)
        backup.status = 'processing'
        backup.save(update_fields=['status'])
        
        # Create backup directory if it doesn't exist
        backup_dir = 'backups'
        os.makedirs(backup_dir, exist_ok=True)
        
        # Create filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        csv_filename = f"{backup_dir}/backup_{backup.id}_{timestamp}.csv"
        
        # Models to backup (exclude system models)
        models_to_backup = [
            ('users', 'User'),
            ('hostel', 'Hotel'),
            ('hostel', 'Floor'),
            ('hostel', 'RoomType'),
            ('hostel', 'Room'),
            ('hostel', 'GuestProfile'),
            ('hostel', 'Booking'),
            ('hostel', 'Invoice'),
            ('hostel', 'Payment'),
            ('administrator', 'AuditLog'),
        ]
        
        # Create timezone-aware date range
        start_datetime = timezone.make_aware(
            datetime.combine(backup.start_date, datetime.min.time())
        )
        end_datetime = timezone.make_aware(
            datetime.combine(backup.end_date, datetime.max.time())
        )
        
        total_records = 0
        backed_up_models = []
        
        # Write CSV with all model data
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            for app_label, model_name in models_to_backup:
                try:
                    # Get the model class
                    model = apps.get_model(app_label, model_name)
                    
                    # Query records created within date range (not deleted)
                    records = model.objects.filter(
                        Q(created_at__gte=start_datetime) & 
                        Q(created_at__lte=end_datetime),
                        is_deleted=False
                    )
                    
                    record_count = records.count()
                    
                    if record_count > 0:
                        # Write model header
                        writer.writerow([])
                        writer.writerow([f"=== {model_name.upper()} ({record_count} records) ==="])
                        
                        # Write field headers - exclude id, many-to-many, and reverse relations
                        fields = []
                        for f in model._meta.get_fields():
                            if f.name == 'id':
                                continue
                            if f.many_to_one:  # ForeignKey fields
                                fields.append(f"{f.name}_id")  # Use the _id version for CSV
                            elif not (f.many_to_many or f.one_to_many or f.one_to_one and not f.auto_created):
                                fields.append(f.name)
                        
                        if not fields:
                            fields = [f.name for f in model._meta.get_fields() if f.name != 'id']
                        
                        writer.writerow(fields)
                        
                        # Write records
                        for record in records.values_list(*fields):
                            writer.writerow(record)
                        
                        backed_up_models.append(model_name)
                        total_records += record_count
                        
                        import logging
                        logging.getLogger(__name__).info(f"Backed up {record_count} {model_name} records")
                        
                except Exception as model_exc:
                    import logging
                    logging.getLogger(__name__).warning(f"Warning: Could not backup {model_name}: {str(model_exc)}")
        
        # Update backup record with success
        file_size = os.path.getsize(csv_filename)
        backup.status = 'completed'
        backup.file_path = csv_filename
        backup.file_size = file_size
        backup.record_count = total_records
        backup.models_backed_up = backed_up_models
        backup.save()
        
        op.success(
            f"Backup completed successfully - "
            f"{total_records} records from {len(backed_up_models)} models backed up"
        )
        
        return {
            'backup_id': backup_id,
            'file_path': csv_filename,
            'record_count': total_records,
            'models_backed_up': backed_up_models,
            'file_size': file_size
        }
        
    except Backup.DoesNotExist:
        op.fail(f"Backup record with ID {backup_id} not found")
        raise
    except Exception as exc:
        op.fail(f"Failed to generate backup", exc=exc)
        
        # Update backup record with error
        try:
            backup = Backup.objects.get(id=backup_id)
            backup.status = 'failed'
            backup.error_message = str(exc)
            backup.save()
        except:
            pass
        
        raise self.retry(exc=exc, countdown=60)
