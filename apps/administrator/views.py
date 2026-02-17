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
from apps.administrator.BBL.Commands.backup_command import BackupCommand
from apps.hostel.BBL.Commands.report_command import ReportCommand
from apps.hostel.BBL.Commands.setting_command import SettingCommand as SettingCommandClass
from apps.hostel.BBL.Queries.setting_query import SettingQuery
from apps.administrator.serializers import *
from apps.hostel.BBL.Queries.dashboard_query import DashboardQuery
from apps.administrator.BBL.Queries.backup_query import BackupQuery, AuditLogQuery
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
    permission_classes = [IsAuthenticatedAndNotDeleted, IsAdminPermission]
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
    permission_classes = [IsAuthenticatedAndNotDeleted, IsAdminPermission]
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
    permission_classes = [IsAuthenticatedAndNotDeleted, IsAdminPermission]
    serializer_class = BookingSerializer
    
    def delete(self, request, booking_id):
        result = BookingCommand.ToggleDelete(booking_id, request.user)
        return Response(result.to_dict(), status=result.status_code)


class BookingCheckInAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedAndNotDeleted]
    serializer_class = BookingSerializer
    
    def post(self, request, booking_id):
        result = BookingCommand.CheckIn(booking_id, request.user)
        return Response(result.to_dict(), status=result.status_code)


class BookingCheckOutAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedAndNotDeleted]
    serializer_class = BookingSerializer
    
    def post(self, request, booking_id):
        result = BookingCommand.CheckOut(booking_id, request.user)
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
    permission_classes = [IsAuthenticatedAndNotDeleted, IsAdminPermission]
    serializer_class = PaymentSerializer
    
    def delete(self, request, payment_id):
        result = PaymentCommand.ToggleDelete(payment_id, request.user)
        return Response(result.to_dict(), status=result.status_code)


# Report endpoints
class OccupancyReportAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedAndNotDeleted]
    
    def get(self, request):
        date = request.query_params.get('date', None)
        result = ReportCommand.GenerateOccupancyReport(date)
        return Response(result.to_dict(), status=result.status_code)


class RevenueReportAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedAndNotDeleted]
    
    def get(self, request):
        date = request.query_params.get('date', None)
        result = ReportCommand.GenerateRevenueReport(date)
        return Response(result.to_dict(), status=result.status_code)


class SalesReportAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedAndNotDeleted]
    
    def get(self, request):
        date = request.query_params.get('date', None)
        result = ReportCommand.GenerateSalesReport(date)
        return Response(result.to_dict(), status=result.status_code)


class ExportReportAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedAndNotDeleted]
    
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
        
        result = BackupCommand.Create(start_date=start_date, end_date=end_date, user=request.user)
        return Response(result.to_dict(), status=result.status_code)


class BackupListAPIView(generics.GenericAPIView):
    """List all backup records"""
    permission_classes = [IsAuthenticatedAndNotDeleted, IsAdminPermission]
    serializer_class = BackupSerializer
    
    def get(self, request):
        result = BackupQuery.GetAll()
        return Response(result.to_dict(), status=result.status_code)


class BackupDetailAPIView(generics.GenericAPIView):
    """Get detailed backup record"""
    permission_classes = [IsAuthenticatedAndNotDeleted, IsAdminPermission]
    serializer_class = BackupSerializer
    
    def get(self, request, backup_id):
        result = BackupQuery.GetById(backup_id)
        return Response(result.to_dict(), status=result.status_code)


class DownloadBackupAPIView(generics.GenericAPIView):
    """Download backup CSV file"""
    permission_classes = [IsAuthenticatedAndNotDeleted, IsAdminPermission]
    
    def get(self, request, backup_id):
        from django.http import FileResponse
        
        result = BackupCommand.Download(backup_id, user=request.user)
        
        if not result.is_success:
            return Response(result.to_dict(), status=result.status_code)
        
        try:
            file_path = result.data['file_path']
            backup_name = result.data['backup_name']
            
            file = open(file_path, 'rb')
            return FileResponse(
                file,
                as_attachment=True,
                filename=f"{backup_name}.csv"
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
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        
        result = AuditLogQuery.GetAll(start_date=start_date, end_date=end_date)
        return Response(result.to_dict(), status=result.status_code)


class AuditLogDetailAPIView(generics.GenericAPIView):
    """Get detailed audit log with full metadata"""
    permission_classes = [IsAuthenticatedAndNotDeleted, IsAdminPermission]
    
    def get(self, request, audit_id):
        result = AuditLogQuery.GetById(audit_id)
        return Response(result.to_dict(), status=result.status_code)
