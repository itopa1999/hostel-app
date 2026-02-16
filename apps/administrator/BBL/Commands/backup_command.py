from http import HTTPStatus
from apps.administrator.models import Backup
from apps.administrator.serializers import BackupSerializer
from apps.administrator.tasks import generate_backup_csv
from utils.base_result import BaseResultWithData
from utils.log_helpers import OperationLogger
from utils.audit.audit_logger import AuditLogger
from utils.serialization_helpers import serialize_for_audit
import os


class BackupCommand:
    
    @staticmethod
    def Create(start_date, end_date, user=None):
        """Create a new backup request"""
        op = OperationLogger("BackupCommand.Create", start_date=str(start_date), end_date=str(end_date))
        op.start()
        
        try:
            # Create backup record
            backup_name = f"Backup_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}"
            backup = Backup.objects.create(
                backup_name=backup_name,
                start_date=start_date,
                end_date=end_date,
                requested_by=user,
                status='pending'
            )
            
            # Trigger background task
            generate_backup_csv.delay(backup.id)
            
            # Audit log
            if user:
                AuditLogger.log(
                    action="CREATE",
                    entity="Backup",
                    status="SUCCESS",
                    description=f"Backup '{backup_name}' created",
                    performed_by=user,
                    new_values=serialize_for_audit(BackupSerializer(backup).data)
                )
            
            op.success(f"Backup {backup.id} created successfully")
            return BaseResultWithData(
                data=BackupSerializer(backup).data,
                status_code=HTTPStatus.CREATED,
                message="Backup request created successfully. Processing in background..."
            )
        except Exception as e:
            op.fail(str(e))
            if user:
                AuditLogger.log(
                    action="CREATE",
                    entity="Backup",
                    status="FAILED",
                    description=f"Failed to create backup: {str(e)}",
                    performed_by=user
                )
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                message="Failed to create backup request"
            )
    
    @staticmethod
    def Download(backup_id, user=None):
        """Get backup file for download"""
        op = OperationLogger("BackupCommand.Download", backup_id=backup_id)
        op.start()
        
        try:
            backup = Backup.objects.get(id=backup_id)
        except Backup.DoesNotExist:
            op.fail(f"Backup with id {backup_id} not found")
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.NOT_FOUND,
                message="Backup not found"
            )
        
        try:
            if backup.status != 'completed':
                op.fail(f"Backup is still {backup.status}")
                return BaseResultWithData(
                    data=None,
                    status_code=HTTPStatus.BAD_REQUEST,
                    message=f"Backup is still {backup.status}"
                )
            
            file_path = backup.file_path
            if not os.path.exists(file_path):
                op.fail(f"Backup file not found at {file_path}")
                return BaseResultWithData(
                    data=None,
                    status_code=HTTPStatus.NOT_FOUND,
                    message="Backup file not found"
                )
            
            # Audit log
            if user:
                AuditLogger.log(
                    action="DOWNLOAD",
                    entity="Backup",
                    status="SUCCESS",
                    description=f"Backup '{backup.backup_name}' downloaded",
                    performed_by=user,
                    old_values=serialize_for_audit(BackupSerializer(backup).data)
                )
            
            op.success(f"Backup {backup_id} downloaded successfully")
            return BaseResultWithData(
                data={"file_path": file_path, "backup_name": backup.backup_name},
                status_code=HTTPStatus.OK,
                message="Backup file ready for download"
            )
        except Exception as e:
            op.fail(str(e))
            if user:
                AuditLogger.log(
                    action="DOWNLOAD",
                    entity="Backup",
                    status="FAILED",
                    description=f"Failed to download backup: {str(e)}",
                    performed_by=user
                )
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                message="Failed to download backup"
            )
