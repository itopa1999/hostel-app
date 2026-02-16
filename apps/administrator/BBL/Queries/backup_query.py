from http import HTTPStatus
from apps.administrator.models import Backup, AuditLog
from apps.administrator.serializers import BackupSerializer
from utils.base_result import BaseResultWithData
from utils.log_helpers import OperationLogger
from django.utils import timezone
from datetime import datetime


class BackupQuery:
    
    @staticmethod
    def GetAll():
        """Get all backups"""
        op = OperationLogger("BackupQuery.GetAll")
        op.start()
        
        try:
            backups = Backup.objects.all().order_by('-created_at')
            serializer = BackupSerializer(backups, many=True)
            
            op.success(f"Retrieved {len(backups)} backups")
            return BaseResultWithData(
                data=serializer.data,
                status_code=HTTPStatus.OK,
                message="Backups retrieved successfully"
            )
        except Exception as e:
            op.fail(str(e))
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                message="Failed to retrieve backups"
            )
    
    @staticmethod
    def GetById(backup_id):
        """Get a specific backup by ID"""
        op = OperationLogger("BackupQuery.GetById", backup_id=backup_id)
        op.start()
        
        try:
            backup = Backup.objects.get(id=backup_id)
            serializer = BackupSerializer(backup)
            
            op.success(f"Retrieved backup {backup_id}")
            return BaseResultWithData(
                data=serializer.data,
                status_code=HTTPStatus.OK,
                message="Backup retrieved successfully"
            )
        except Backup.DoesNotExist:
            op.fail(f"Backup with id {backup_id} not found")
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.NOT_FOUND,
                message="Backup not found"
            )
        except Exception as e:
            op.fail(str(e))
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                message="Failed to retrieve backup"
            )


class AuditLogQuery:
    
    @staticmethod
    def GetAll(start_date=None, end_date=None):
        """Get all audit logs with optional date range filter"""
        op = OperationLogger("AuditLogQuery.GetAll", start_date=str(start_date), end_date=str(end_date))
        op.start()
        
        try:
            query = AuditLog.objects.all().order_by('-created_at')
            
            # Apply date filters if provided
            if start_date and end_date:
                try:
                    if isinstance(start_date, str):
                        start_date = datetime.strptime(start_date, '%Y-%m-%d')
                    if isinstance(end_date, str):
                        end_date = datetime.strptime(end_date, '%Y-%m-%d')
                    
                    # Make dates timezone-aware
                    start_date = timezone.make_aware(
                        datetime.combine(start_date.date(), datetime.min.time())
                    )
                    end_date = timezone.make_aware(
                        datetime.combine(end_date.date(), datetime.max.time())
                    )
                    
                    query = query.filter(created_at__gte=start_date, created_at__lte=end_date)
                except ValueError:
                    pass
            else:
                # Default: show today's audits
                today = timezone.now().date()
                start_of_day = timezone.make_aware(
                    datetime.combine(today, datetime.min.time())
                )
                end_of_day = timezone.make_aware(
                    datetime.combine(today, datetime.max.time())
                )
                query = query.filter(created_at__gte=start_of_day, created_at__lte=end_of_day)
            
            audits = query[:1000]  # Limit to 1000 records for performance
            
            # Serialize data
            audit_data = []
            for audit in audits:
                audit_data.append({
                    'id': audit.id,
                    'action': audit.action,
                    'entity': audit.entity,
                    'status': audit.status,
                    'description': audit.description,
                    'performed_by': audit.performed_by.username if audit.performed_by else 'System',
                    'target_user': audit.target_user.username if audit.target_user else None,
                    'old_values': audit.old_values,
                    'new_values': audit.new_values,
                    'metadata': audit.metadata,
                    'created_at': audit.created_at.isoformat(),
                })
            
            op.success(f"Retrieved {len(audit_data)} audit logs")
            return BaseResultWithData(
                data=audit_data,
                status_code=HTTPStatus.OK,
                message="Audit logs retrieved successfully"
            )
        except Exception as e:
            op.fail(str(e))
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                message="Failed to retrieve audit logs"
            )
    
    @staticmethod
    def GetById(audit_id):
        """Get a specific audit log by ID"""
        op = OperationLogger("AuditLogQuery.GetById", audit_id=audit_id)
        op.start()
        
        try:
            audit = AuditLog.objects.get(id=audit_id)
            
            audit_data = {
                'id': audit.id,
                'action': audit.action,
                'entity': audit.entity,
                'status': audit.status,
                'description': audit.description,
                'performed_by': audit.performed_by.username if audit.performed_by else 'System',
                'performed_by_id': audit.performed_by.id if audit.performed_by else None,
                'target_user': audit.target_user.username if audit.target_user else None,
                'target_user_id': audit.target_user.id if audit.target_user else None,
                'old_values': audit.old_values,
                'new_values': audit.new_values,
                'metadata': audit.metadata,
                'created_at': audit.created_at.isoformat(),
            }
            
            op.success(f"Retrieved audit log {audit_id}")
            return BaseResultWithData(
                data=audit_data,
                status_code=HTTPStatus.OK,
                message="Audit log retrieved successfully"
            )
        except AuditLog.DoesNotExist:
            op.fail(f"Audit log with id {audit_id} not found")
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.NOT_FOUND,
                message="Audit log not found"
            )
        except Exception as e:
            op.fail(str(e))
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                message="Failed to retrieve audit log"
            )
