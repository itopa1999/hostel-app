from django.shortcuts import render
from rest_framework import generics
from django.contrib.auth import get_user_model


from rest_framework.views import APIView
from apps.administrator.BBL.Commands.hotel_command import HotelCommand
from apps.administrator.BBL.Commands.floor_command import FloorCommand
from apps.administrator.BBL.Commands.room_type_command import RoomTypeCommand
from apps.administrator.BBL.Commands.room_command import RoomCommand
from apps.administrator.serializers import *
from apps.hostel.serializers import FloorSerializer, RoomTypeSerializer, RoomSerializer
from apps.hostel.BBL.Queries.dashboard_query import DashboardQuery
from apps.hostel.BBL.Queries.floor_query import FloorQuery
from apps.hostel.BBL.Queries.room_type_query import RoomTypeQuery
from apps.hostel.BBL.Queries.room_query import RoomQuery
from utils.permissions import IsAdminPermission
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.administrator.BBL.Commands.user_command import UserCommand
from rest_framework import status
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


class DashboardAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminPermission]
    
    def get(self, request):
        result = DashboardQuery.GetDashboardMetrics()
        return Response(result.to_dict(), status=result.status_code)


class FloorCreateAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FloorSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            result = FloorCommand.Create(serializer.validated_data, request.user)
            return Response(result.to_dict(), status=result.status_code)
        return Response({"success": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class FloorUpdateAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FloorSerializer
    
    def put(self, request, floor_id):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            result = FloorCommand.Update(floor_id, serializer.validated_data, request.user)
            return Response(result.to_dict(), status=result.status_code)
        return Response({"success": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class FloorListAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FloorSerializer
    
    def get(self, request):
        result = FloorQuery.GetAll()
        if result.success:
            serializer = self.get_serializer(result.data, many=True)
            return Response({
                "success": result.success,
                "message": result.message,
                "data": serializer.data
            }, status=result.status_code)
        return Response(result.to_dict(), status=result.status_code)


class FloorDetailAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FloorSerializer
    
    def get(self, request, floor_id):
        result = FloorQuery.GetById(floor_id)
        if result.success:
            serializer = self.get_serializer(result.data)
            return Response({
                "success": result.success,
                "message": result.message,
                "data": serializer.data
            }, status=result.status_code)
        return Response(result.to_dict(), status=result.status_code)


class FloorDeleteAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, floor_id):
        result = FloorCommand.ToggleDelete(floor_id, request.user)
        return Response(result.to_dict(), status=result.status_code)


class RoomTypeCreateAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RoomTypeSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            result = RoomTypeCommand.Create(serializer.validated_data, request.user)
            return Response(result.to_dict(), status=result.status_code)
        return Response({"success": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class RoomTypeUpdateAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RoomTypeSerializer
    
    def put(self, request, room_type_id):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            result = RoomTypeCommand.Update(room_type_id, serializer.validated_data, request.user)
            return Response(result.to_dict(), status=result.status_code)
        return Response({"success": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class RoomTypeListAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RoomTypeSerializer
    
    def get(self, request):
        result = RoomTypeQuery.GetAll()
        if result.success:
            serializer = self.get_serializer(result.data, many=True)
            return Response({
                "success": result.success,
                "message": result.message,
                "data": serializer.data
            }, status=result.status_code)
        return Response(result.to_dict(), status=result.status_code)


class RoomTypeDetailAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RoomTypeSerializer
    
    def get(self, request, room_type_id):
        result = RoomTypeQuery.GetById(room_type_id)
        if result.success:
            serializer = self.get_serializer(result.data)
            return Response({
                "success": result.success,
                "message": result.message,
                "data": serializer.data
            }, status=result.status_code)
        return Response(result.to_dict(), status=result.status_code)


class RoomTypeDeleteAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, room_type_id):
        result = RoomTypeCommand.ToggleDelete(room_type_id, request.user)
        return Response(result.to_dict(), status=result.status_code)


class RoomCreateAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RoomSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            result = RoomCommand.Create(serializer.validated_data, request.user)
            return Response(result.to_dict(), status=result.status_code)
        return Response({"success": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class RoomUpdateAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RoomSerializer
    
    def put(self, request, room_id):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            result = RoomCommand.Update(room_id, serializer.validated_data, request.user)
            return Response(result.to_dict(), status=result.status_code)
        return Response({"success": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class RoomListAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RoomSerializer
    
    def get(self, request):
        result = RoomQuery.GetAll()
        if result.success:
            serializer = self.get_serializer(result.data, many=True)
            return Response({
                "success": result.success,
                "message": result.message,
                "data": serializer.data
            }, status=result.status_code)
        return Response(result.to_dict(), status=result.status_code)


class RoomDetailAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RoomSerializer
    
    def get(self, request, room_id):
        result = RoomQuery.GetById(room_id)
        if result.success:
            serializer = self.get_serializer(result.data)
            return Response({
                "success": result.success,
                "message": result.message,
                "data": serializer.data
            }, status=result.status_code)
        return Response(result.to_dict(), status=result.status_code)


class RoomDeleteAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, room_id):
        result = RoomCommand.ToggleDelete(room_id, request.user)
        return Response(result.to_dict(), status=result.status_code)

