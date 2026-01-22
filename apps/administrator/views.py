from django.shortcuts import render
from rest_framework import generics, status
from django.contrib.auth import get_user_model
from http import HTTPStatus

from rest_framework.views import APIView
from apps.administrator.BBL.Commands.hotel_command import HotelCommand
from apps.administrator.BBL.Commands.floor_command import FloorCommand
from apps.administrator.BBL.Commands.room_type_command import RoomTypeCommand
from apps.administrator.BBL.Commands.room_command import RoomCommand
from apps.administrator.BBL.Commands.guest_profile_command import GuestProfileCommand
from apps.administrator.BBL.Commands.booking_command import BookingCommand
from apps.administrator.BBL.Commands.invoice_command import InvoiceCommand
from apps.administrator.BBL.Commands.payment_command import PaymentCommand
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
from apps.hostel.serializers import FloorSerializer, GuestProfileSerializer, RoomSerializer, RoomTypeSerializer, BookingSerializer, InvoiceSerializer, PaymentSerializer
from utils.permissions import IsAdminPermission
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.administrator.BBL.Commands.user_command import UserCommand
from utils.base_result import BaseResultWithData
# Create your views here.

User = get_user_model()

class UserCreateViewAPI(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdminPermission]
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
    permission_classes = [IsAuthenticated, IsAdminPermission]
    serializer_class = ChangeUserPasswordSerializer
    
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        new_password = request.data.get('new_password')
        
        result = UserCommand.ChangePassword(
            user_id=user_id,
            new_password=new_password,
            performed_by=request.user
        )
        return Response(result.to_dict(), status=result.status_code)
    
    
class UpdateUserViewAPI(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdminPermission]
    serializer_class = UserUpdateSerializer
    
    def put(self, request, user_id, *args, **kwargs):
        user_id = user_id
        username = request.data.get('username')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email')
        is_active = request.data.get('is_active')
        groups = request.data.get('groups', [])
        
        result = UserCommand.Update(
            user_id=user_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_active=is_active,
            groups=groups,
            performed_by=request.user
        )
        
        return Response(result.to_dict(), status=result.status_code)
    
    
class ToggleDeleteUserViewAPI(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdminPermission]
    
    def delete(self, request, user_id, *args, **kwargs):
        result = UserCommand.ToggleDelete(
            user_id=user_id,
            performed_by=request.user
        )
        return Response(result.to_dict(), status=result.status_code)
    
    
    

# Hotel Endpoints
class HotelUpdateAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdminPermission]
    serializer_class = HotelUpdateSerializer
    
    def put(self, request, *args, **kwargs):
        result = HotelCommand.Update(data=request.data, user=request.user)
        return Response(result.to_dict(), status=result.status_code)
    
    def patch(self, request, hotel_id, *args, **kwargs):
        result = HotelCommand.Update( data=request.data, user=request.user)
        return Response(result.to_dict(), status=result.status_code)


class HotelDetailAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdminPermission]
    serializer_class = HotelDetailSerializer
    def get(self, request):
        result = HotelQuery.GetFirst()
        return Response(result.to_dict(), status=result.status_code)


class DashboardAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminPermission]
    
    def get(self, request):
        result = DashboardQuery.GetDashboardMetrics()
        return Response(result.to_dict(), status=result.status_code)


class FloorCreateAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FloorSerializer
    def post(self, request):
        result = FloorCommand.Create(request.data, request.user)
        return Response(result.to_dict(), status=result.status_code)


class FloorUpdateAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FloorSerializer
    def put(self, request, floor_id):
        result = FloorCommand.Update(floor_id, request.data, request.user)
        return Response(result.to_dict(), status=result.status_code)


class FloorListAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FloorSerializer
    def get(self, request):
        result = FloorQuery.GetAll()
        return Response(result.to_dict(), status=result.status_code)


class FloorDetailAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FloorSerializer
    def get(self, request, floor_id):
        result = FloorQuery.GetById(floor_id)
        return Response(result.to_dict(), status=result.status_code)


class FloorDeleteAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FloorSerializer
    def delete(self, request, floor_id):
        result = FloorCommand.ToggleDelete(floor_id, request.user)
        return Response(result.to_dict(), status=result.status_code)


class RoomTypeCreateAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RoomTypeSerializer
    def post(self, request):
        result = RoomTypeCommand.Create(request.data, request.user)
        return Response(result.to_dict(), status=result.status_code)


class RoomTypeUpdateAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RoomTypeSerializer
    def put(self, request, room_type_id):
        result = RoomTypeCommand.Update(room_type_id, request.data, request.user)
        return Response(result.to_dict(), status=result.status_code)


class RoomTypeListAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RoomTypeSerializer
    def get(self, request):
        result = RoomTypeQuery.GetAll()
        return Response(result.to_dict(), status=result.status_code)


class RoomTypeDetailAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RoomTypeSerializer
    def get(self, request, room_type_id):
        result = RoomTypeQuery.GetById(room_type_id)
        return Response(result.to_dict(), status=result.status_code)


class RoomTypeDeleteAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RoomTypeSerializer
    def delete(self, request, room_type_id):
        result = RoomTypeCommand.ToggleDelete(room_type_id, request.user)
        return Response(result.to_dict(), status=result.status_code)


class RoomCreateAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RoomSerializer
    def post(self, request):
        result = RoomCommand.Create(request.data, request.user)
        return Response(result.to_dict(), status=result.status_code)


class RoomUpdateAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RoomSerializer
    def put(self, request, room_id):
        result = RoomCommand.Update(room_id, request.data, request.user)
        return Response(result.to_dict(), status=result.status_code)


class RoomListAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RoomSerializer
    def get(self, request):
        result = RoomQuery.GetAll()
        return Response(result.to_dict(), status=result.status_code)


class RoomDetailAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RoomSerializer
    def get(self, request, room_id):
        result = RoomQuery.GetById(room_id)
        return Response(result.to_dict(), status=result.status_code)


class RoomDeleteAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RoomSerializer
    def delete(self, request, room_id):
        result = RoomCommand.ToggleDelete(room_id, request.user)
        return Response(result.to_dict(), status=result.status_code)


# Guest Profile endpoints
class GuestProfileCreateAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GuestProfileSerializer
    def post(self, request):
        result = GuestProfileCommand.Create(request.data, request.user)
        return Response(result.to_dict(), status=result.status_code)


class GuestProfileUpdateAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GuestProfileSerializer
    def put(self, request, guest_id):
        result = GuestProfileCommand.Update(guest_id, request.data, request.user)
        return Response(result.to_dict(), status=result.status_code)


class GuestProfileListAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GuestProfileSerializer
    def get(self, request):
        result = GuestProfileQuery.GetAll()
        return Response(result.to_dict(), status=result.status_code)


class GuestProfileDetailAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GuestProfileSerializer
    def get(self, request, guest_id):
        result = GuestProfileQuery.GetById(guest_id)
        return Response(result.to_dict(), status=result.status_code)


class GuestProfileDeleteAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GuestProfileSerializer
    def delete(self, request, guest_id):
        result = GuestProfileCommand.ToggleDelete(guest_id, request.user)
        return Response(result.to_dict(), status=result.status_code)


# Booking endpoints
class BookingCreateAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookingSerializer
    
    def post(self, request):
        result = BookingCommand.Create(request.data, request.user)
        return Response(result.to_dict(), status=result.status_code)


class BookingUpdateAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookingSerializer
    
    def put(self, request, booking_id):
        result = BookingCommand.Update(booking_id, request.data, request.user)
        return Response(result.to_dict(), status=result.status_code)


class BookingListAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookingSerializer
    
    def get(self, request):
        result = BookingQuery.GetAll()
        return Response(result.to_dict(), status=result.status_code)


class BookingDetailAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookingSerializer
    
    def get(self, request, booking_id):
        result = BookingQuery.GetById(booking_id)
        return Response(result.to_dict(), status=result.status_code)


class BookingToggleDeleteAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookingSerializer
    
    def delete(self, request, booking_id):
        result = BookingCommand.ToggleDelete(booking_id, request.user)
        return Response(result.to_dict(), status=result.status_code)


# Invoice endpoints
class InvoiceCreateAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InvoiceSerializer
    
    def post(self, request):
        result = InvoiceCommand.Create(request.data, request.user)
        return Response(result.to_dict(), status=result.status_code)


class InvoiceListAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InvoiceSerializer
    
    def get(self, request):
        result = InvoiceQuery.GetAll()
        return Response(result.to_dict(), status=result.status_code)


class InvoiceDetailAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InvoiceSerializer
    
    def get(self, request, invoice_id):
        result = InvoiceQuery.GetById(invoice_id)
        return Response(result.to_dict(), status=result.status_code)


# Payment endpoints
class PaymentListAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer
    
    def get(self, request):
        result = PaymentQuery.GetAll()
        return Response(result.to_dict(), status=result.status_code)


class PaymentDetailAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer
    
    def get(self, request, payment_id):
        result = PaymentQuery.GetById(payment_id)
        return Response(result.to_dict(), status=result.status_code)


class PaymentUpdateStatusAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdminPermission]
    serializer_class = PaymentSerializer
    
    def put(self, request, payment_id):
        result = PaymentCommand.Update(payment_id, request.data, user=request.user)
        return Response(result.to_dict(), status=result.status_code)


class PaymentToggleDeleteAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer
    
    def delete(self, request, payment_id):
        result = PaymentCommand.ToggleDelete(payment_id, request.user)
        return Response(result.to_dict(), status=result.status_code)

