from django.shortcuts import render
from rest_framework import generics, status
from django.contrib.auth import get_user_model
from http import HTTPStatus
from datetime import datetime

from rest_framework.views import APIView
from apps.administrator.BBL.Commands.hotel_command import HotelCommand
from apps.administrator.BBL.Commands.floor_command import FloorCommand
from apps.administrator.BBL.Commands.room_type_command import RoomTypeCommand
from apps.administrator.BBL.Commands.room_command import RoomCommand
from apps.administrator.BBL.Commands.guest_profile_command import GuestProfileCommand
from apps.administrator.BBL.Commands.booking_command import BookingCommand
from apps.administrator.BBL.Commands.invoice_command import InvoiceCommand
from apps.administrator.BBL.Commands.payment_command import PaymentCommand
from apps.hostel.BBL.Commands.report_command import ReportCommand
from apps.hostel.BBL.Commands.setting_command import SettingCommand as SettingCommandClass
from apps.hostel.BBL.Queries.setting_query import SettingQuery
from apps.administrator.serializers import *
from apps.hostel.BBL.Queries.dashboard_query import DashboardQuery
from apps.hostel.BBL.Queries.hotel_query import HotelQuery
from apps.hostel.BBL.Queries.floor_query import FloorQuery
from apps.hostel.BBL.Queries.room_type_query import RoomTypeQuery
from apps.hostel.BBL.Queries.room_query import RoomQuery
from apps.hostel.BBL.Queries.guest_profile_query import GuestProfileQuery
from apps.hostel.BBL.Queries.booking_query import BookingQuery
from apps.hostel.BBL.Queries.invoice_query import InvoiceQuery
from apps.hostel.BBL.Queries.payment_query import PaymentQuery
from apps.hostel.serializers import FloorSerializer, GuestProfileSerializer, RoomSerializer, RoomTypeSerializer, BookingSerializer, InvoiceSerializer, PaymentSerializer, SettingSerializer
from utils.permissions import IsAdminPermission, IsAuthenticatedAndNotDeleted
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.administrator.BBL.Commands.user_command import UserCommand
from utils.base_result import BaseResultWithData
from apps.administrator.models import Backup, AuditLog
from apps.administrator.tasks import generate_backup_csv
# Create your views here.

User = get_user_model()

class UserCreateViewAPI(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedAndNotDeleted, IsAdminPermission]
    serializer_class = UserCreateSerializer
    
    def post(self, request, *args, **kwargs):
        result = UserCommand.Create(
            username=request.data.get('username'),
            first_name=request.data.get('first_name'),
            last_name=request.data.get('last_name'),
            password=request.data.get('password'),
            groups=request.data.get('groups', []),
            email=request.data.get('email'),
            request=request
        )
        
        return Response(result.to_dict(), status=result.status_code)
    


class ChangeUserPasswordViewAPI(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedAndNotDeleted]
    serializer_class = ChangeUserPasswordSerializer
    
    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        
        result = UserCommand.ChangePassword(
            user_id=user_id,
            old_password=old_password,
            new_password=new_password,
            performed_by=request.user
        )
        return Response(result.to_dict(), status=result.status_code.value)
    
    
class ToggleDeleteUserViewAPI(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedAndNotDeleted, IsAdminPermission]
    
    def delete(self, request, user_id, *args, **kwargs):
        result = UserCommand.ToggleDelete(
            user_id=user_id,
            performed_by=request.user
        )
        return Response(result.to_dict(), status=result.status_code)
    
    
    

# Hotel Endpoints
class HotelUpdateAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedAndNotDeleted, IsAdminPermission]
    serializer_class = HotelUpdateSerializer
    
    def put(self, request, *args, **kwargs):
        result = HotelCommand.Update(data=request.data, user=request.user)
        return Response(result.to_dict(), status=result.status_code)
    
    def patch(self, request, hotel_id, *args, **kwargs):
        result = HotelCommand.Update( data=request.data, user=request.user)
        return Response(result.to_dict(), status=result.status_code)


class HotelDetailAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedAndNotDeleted, IsAdminPermission]
    serializer_class = HotelDetailSerializer
    def get(self, request):
        result = HotelQuery.GetFirst()
        return Response(result.to_dict(), status=result.status_code)


class DashboardAPIView(APIView):
    permission_classes = [IsAuthenticatedAndNotDeleted]
    
    def get(self, request):
        result = DashboardQuery.GetDashboardMetrics()
        return Response(result.to_dict(), status=result.status_code)


class FloorCreateAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedAndNotDeleted, IsAdminPermission]
    serializer_class = FloorSerializer
    def post(self, request):
        result = FloorCommand.Create(request.data, request.user)
        return Response(result.to_dict(), status=result.status_code)


class FloorUpdateAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedAndNotDeleted, IsAdminPermission]
    serializer_class = FloorSerializer
    def put(self, request, floor_id):
        result = FloorCommand.Update(floor_id, request.data, request.user)
        return Response(result.to_dict(), status=result.status_code)


class FloorListAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedAndNotDeleted]
    serializer_class = FloorSerializer
    def get(self, request):
        result = FloorQuery.GetAll()
        return Response(result.to_dict(), status=result.status_code)


class FloorDetailAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedAndNotDeleted]
    serializer_class = FloorSerializer
    def get(self, request, floor_id):
        result = FloorQuery.GetById(floor_id)
        return Response(result.to_dict(), status=result.status_code)


class FloorDeleteAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedAndNotDeleted, IsAdminPermission]
    serializer_class = FloorSerializer
    def delete(self, request, floor_id):
        result = FloorCommand.ToggleDelete(floor_id, request.user)
        return Response(result.to_dict(), status=result.status_code)


class RoomTypeCreateAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedAndNotDeleted, IsAdminPermission]
    serializer_class = RoomTypeSerializer
    def post(self, request):
        result = RoomTypeCommand.Create(request.data, request.user)
        return Response(result.to_dict(), status=result.status_code)


class RoomTypeUpdateAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedAndNotDeleted, IsAdminPermission]
    serializer_class = RoomTypeSerializer
    def put(self, request, room_type_id):
        result = RoomTypeCommand.Update(room_type_id, request.data, request.user)
        return Response(result.to_dict(), status=result.status_code)


class RoomTypeListAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedAndNotDeleted]
    serializer_class = RoomTypeSerializer
    def get(self, request):
        result = RoomTypeQuery.GetAll()
        return Response(result.to_dict(), status=result.status_code)


class RoomTypeDetailAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedAndNotDeleted]
    serializer_class = RoomTypeSerializer
    def get(self, request, room_type_id):
        result = RoomTypeQuery.GetById(room_type_id)
        return Response(result.to_dict(), status=result.status_code)


class RoomTypeDeleteAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedAndNotDeleted, IsAdminPermission]
    serializer_class = RoomTypeSerializer
    def delete(self, request, room_type_id):
        result = RoomTypeCommand.ToggleDelete(room_type_id, request.user)
        return Response(result.to_dict(), status=result.status_code)


class RoomCreateAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedAndNotDeleted]
    serializer_class = RoomSerializer
    def post(self, request):
        result = RoomCommand.Create(request.data, request.user)
        return Response(result.to_dict(), status=result.status_code)


class RoomUpdateAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedAndNotDeleted]
    serializer_class = RoomSerializer
    def put(self, request, room_id):
        result = RoomCommand.Update(room_id, request.data, request.user)
        return Response(result.to_dict(), status=result.status_code)


class RoomListAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedAndNotDeleted]
    serializer_class = RoomSerializer
    def get(self, request):
        result = RoomQuery.GetAll()
        return Response(result.to_dict(), status=result.status_code)


class RoomDetailAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedAndNotDeleted]
    serializer_class = RoomSerializer
    def get(self, request, room_id):
        result = RoomQuery.GetById(room_id)
        return Response(result.to_dict(), status=result.status_code)


class RoomDeleteAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedAndNotDeleted]
    serializer_class = RoomSerializer
    def delete(self, request, room_id):
        result = RoomCommand.ToggleDelete(room_id, request.user)
        return Response(result.to_dict(), status=result.status_code)


# Guest Profile endpoints
class GuestProfileCreateAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedAndNotDeleted]
    serializer_class = GuestProfileSerializer
    def post(self, request):
        result = GuestProfileCommand.Create(request.data, request.user)
        return Response(result.to_dict(), status=result.status_code)


class GuestProfileUpdateAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedAndNotDeleted]
    serializer_class = GuestProfileSerializer
    def put(self, request, guest_id):
        result = GuestProfileCommand.Update(guest_id, request.data, request.user)
        return Response(result.to_dict(), status=result.status_code)


class GuestProfileListAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedAndNotDeleted]
    serializer_class = GuestProfileSerializer
    def get(self, request):
        result = GuestProfileQuery.GetAll()
        return Response(result.to_dict(), status=result.status_code)


class GuestProfileDetailAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedAndNotDeleted]
    serializer_class = GuestProfileSerializer
    def get(self, request, guest_id):
        result = GuestProfileQuery.GetById(guest_id)
        return Response(result.to_dict(), status=result.status_code)


class GuestProfileDeleteAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedAndNotDeleted]
    serializer_class = GuestProfileSerializer
    def delete(self, request, guest_id):
        result = GuestProfileCommand.ToggleDelete(guest_id, request.user)
        return Response(result.to_dict(), status=result.status_code)


# Booking endpoints
class BookingCreateAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedAndNotDeleted]
    serializer_class = BookingSerializer
    
    def post(self, request):
        result = BookingCommand.Create(request.data, request.user)
        return Response(result.to_dict(), status=result.status_code)


class BookingUpdateAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedAndNotDeleted]
    serializer_class = BookingSerializer
    
    def put(self, request, booking_id):
        result = BookingCommand.Update(booking_id, request.data, request.user)
        return Response(result.to_dict(), status=result.status_code)


class BookingListAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedAndNotDeleted]
    serializer_class = BookingSerializer
    
    def get(self, request):
        result = BookingQuery.GetAll()
        return Response(result.to_dict(), status=result.status_code)


class BookingDetailAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedAndNotDeleted]
    serializer_class = BookingSerializer
    
    def get(self, request, booking_id):
        result = BookingQuery.GetById(booking_id)
        return Response(result.to_dict(), status=result.status_code)


class BookingToggleDeleteAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedAndNotDeleted]
    serializer_class = BookingSerializer
    
    def delete(self, request, booking_id):
        result = BookingCommand.ToggleDelete(booking_id, request.user)
        return Response(result.to_dict(), status=result.status_code)


class BookingCheckInAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedAndNotDeleted, IsAdminPermission]
    serializer_class = BookingSerializer
    
    def post(self, request, booking_id):
        result = BookingCommand.CheckIn(booking_id, request.user)
        return Response(result.to_dict(), status=result.status_code)


# Invoice endpoints
class InvoiceCreateAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedAndNotDeleted]
    serializer_class = InvoiceSerializer
    
    def post(self, request):
        result = InvoiceCommand.Create(request.data, request.user)
        return Response(result.to_dict(), status=result.status_code)


class InvoiceListAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedAndNotDeleted]
    serializer_class = InvoiceSerializer
    
    def get(self, request):
        result = InvoiceQuery.GetAll()
        return Response(result.to_dict(), status=result.status_code)


class InvoiceDetailAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedAndNotDeleted]
    serializer_class = InvoiceSerializer
    
    def get(self, request, invoice_id):
        result = InvoiceQuery.GetById(invoice_id)
        return Response(result.to_dict(), status=result.status_code)


# Payment endpoints
class PaymentListAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedAndNotDeleted]
    serializer_class = PaymentSerializer
    
    def get(self, request):
        result = PaymentQuery.GetAll()
        return Response(result.to_dict(), status=result.status_code)


class PaymentDetailAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedAndNotDeleted]
    serializer_class = PaymentSerializer
    
    def get(self, request, payment_id):
        result = PaymentQuery.GetById(payment_id)
        return Response(result.to_dict(), status=result.status_code)


class PaymentUpdateStatusAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedAndNotDeleted, IsAdminPermission]
    serializer_class = PaymentSerializer
    
    def put(self, request, payment_id):
        result = PaymentCommand.Update(payment_id, request.data, user=request.user)
        return Response(result.to_dict(), status=result.status_code)


class PaymentToggleDeleteAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedAndNotDeleted]
    serializer_class = PaymentSerializer
    
    def delete(self, request, payment_id):
        result = PaymentCommand.ToggleDelete(payment_id, request.user)
        return Response(result.to_dict(), status=result.status_code)


# Report endpoints
class OccupancyReportAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedAndNotDeleted, IsAdminPermission]
    
    def get(self, request):
        date = request.query_params.get('date', None)
        result = ReportCommand.GenerateOccupancyReport(date)
        return Response(result.to_dict(), status=result.status_code)


class RevenueReportAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedAndNotDeleted, IsAdminPermission]
    
    def get(self, request):
        date = request.query_params.get('date', None)
        result = ReportCommand.GenerateRevenueReport(date)
        return Response(result.to_dict(), status=result.status_code)


class SalesReportAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedAndNotDeleted, IsAdminPermission]
    
    def get(self, request):
        date = request.query_params.get('date', None)
        result = ReportCommand.GenerateSalesReport(date)
        return Response(result.to_dict(), status=result.status_code)


class ExportReportAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedAndNotDeleted, IsAdminPermission]
    
    def get(self, request):
        date = request.query_params.get('date', None)
        result = ReportCommand.GenerateExportReport(date)
        return Response(result.to_dict(), status=result.status_code)


class SettingsAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedAndNotDeleted, IsAdminPermission]
    serializer_class = SettingSerializer
    
    def get(self, request):
        result = SettingQuery.Get()
        return Response(result.to_dict(), status=result.status_code.value)
    
    def put(self, request):
        result = SettingCommandClass.Update(request.data, performed_by=request.user)
        return Response(result.to_dict(), status=result.status_code.value)


class CreateBackupAPIView(generics.GenericAPIView):
    """Create a backup request and trigger background task"""
    permission_classes = [IsAuthenticatedAndNotDeleted, IsAdminPermission]
    serializer_class = BackupCreateSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    'is_success': False,
                    'message': 'Invalid backup request',
                    'errors': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        start_date = serializer.validated_data['start_date']
        end_date = serializer.validated_data['end_date']
        
        try:
            # Create backup record
            backup_name = f"Backup_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}"
            backup = Backup.objects.create(
                backup_name=backup_name,
                start_date=start_date,
                end_date=end_date,
                requested_by=request.user,
                status='pending'
            )
            
            # Trigger background task
            generate_backup_csv.delay(backup.id)
            
            return Response(
                {
                    'is_success': True,
                    'message': 'Backup request created successfully. Processing in background...',
                    'data': BackupSerializer(backup).data
                },
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {
                    'is_success': False,
                    'message': 'Failed to create backup request',
                    'error': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class BackupListAPIView(generics.GenericAPIView):
    """List all backup records"""
    permission_classes = [IsAuthenticatedAndNotDeleted, IsAdminPermission]
    serializer_class = BackupSerializer
    
    def get(self, request):
        try:
            backups = Backup.objects.all().order_by('-created_at')
            serializer = self.get_serializer(backups, many=True)
            
            return Response(
                {
                    'is_success': True,
                    'message': 'Backups retrieved successfully',
                    'data': serializer.data,
                    'count': backups.count()
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    'is_success': False,
                    'message': 'Failed to retrieve backups',
                    'error': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class BackupDetailAPIView(generics.GenericAPIView):
    """Get detailed backup record"""
    permission_classes = [IsAuthenticatedAndNotDeleted, IsAdminPermission]
    serializer_class = BackupSerializer
    
    def get(self, request, backup_id):
        try:
            backup = Backup.objects.get(id=backup_id)
            serializer = self.get_serializer(backup)
            
            return Response(
                {
                    'is_success': True,
                    'message': 'Backup retrieved successfully',
                    'data': serializer.data
                },
                status=status.HTTP_200_OK
            )
        except Backup.DoesNotExist:
            return Response(
                {
                    'is_success': False,
                    'message': 'Backup not found'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {
                    'is_success': False,
                    'message': 'Failed to retrieve backup',
                    'error': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DownloadBackupAPIView(generics.GenericAPIView):
    """Download backup CSV file"""
    permission_classes = [IsAuthenticatedAndNotDeleted, IsAdminPermission]
    
    def get(self, request, backup_id):
        import os
        from django.http import FileResponse
        
        try:
            backup = Backup.objects.get(id=backup_id)
            
            if backup.status != 'completed':
                return Response(
                    {
                        'is_success': False,
                        'message': f'Backup is still {backup.status}'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            file_path = backup.file_path
            if not os.path.exists(file_path):
                return Response(
                    {
                        'is_success': False,
                        'message': 'Backup file not found'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            
            file = open(file_path, 'rb')
            return FileResponse(
                file,
                as_attachment=True,
                filename=f"{backup.backup_name}.csv"
            )
        except Backup.DoesNotExist:
            return Response(
                {
                    'is_success': False,
                    'message': 'Backup not found'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {
                    'is_success': False,
                    'message': 'Failed to download backup',
                    'error': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AuditLogListAPIView(generics.GenericAPIView):
    """List audit logs with optional date range filter"""
    permission_classes = [IsAuthenticatedAndNotDeleted, IsAdminPermission]
    
    def get(self, request):
        from django.utils import timezone
        from datetime import timedelta
        
        try:
            # Get date range from query parameters
            start_date_str = request.query_params.get('start_date', None)
            end_date_str = request.query_params.get('end_date', None)
            
            # Build query
            query = AuditLog.objects.all().order_by('-created_at')
            
            # Apply date filters if provided
            if start_date_str and end_date_str:
                try:
                    from datetime import datetime
                    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
                    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
                    
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
            
            return Response(
                {
                    'is_success': True,
                    'message': 'Audit logs retrieved successfully',
                    'data': audit_data,
                    'count': len(audit_data)
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    'is_success': False,
                    'message': 'Failed to retrieve audit logs',
                    'error': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AuditLogDetailAPIView(generics.GenericAPIView):
    """Get detailed audit log with full metadata"""
    permission_classes = [IsAuthenticatedAndNotDeleted, IsAdminPermission]
    
    def get(self, request, audit_id):
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
            
            return Response(
                {
                    'is_success': True,
                    'message': 'Audit log retrieved successfully',
                    'data': audit_data
                },
                status=status.HTTP_200_OK
            )
        except AuditLog.DoesNotExist:
            return Response(
                {
                    'is_success': False,
                    'message': 'Audit log not found'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {
                    'is_success': False,
                    'message': 'Failed to retrieve audit log',
                    'error': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
