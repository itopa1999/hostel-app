from django.shortcuts import render
from rest_framework import generics
from django.contrib.auth import get_user_model


from rest_framework.views import APIView
from apps.administrator.BBL.Commands.hotel_command import HotelCommand
from apps.administrator.serializers import *
from apps.hostel.BBL.Queries.dashboard_query import DashboardQuery
from utils.permissions import IsAdminPermission
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.administrator.BBL.Commands.user_command import UserCommand
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
    
    def put(self, request, hotel_id, *args, **kwargs):
        result = HotelCommand.Update(hotel_id=hotel_id, data=request.data, user=request.user)
        return Response(result.to_dict(), status=result.status_code)
    
    def patch(self, request, hotel_id, *args, **kwargs):
        result = HotelCommand.Update(hotel_id=hotel_id, data=request.data, user=request.user)
        return Response(result.to_dict(), status=result.status_code)


class DashboardAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminPermission]
    
    def get(self, request):
        result = DashboardQuery.GetDashboardMetrics()
        return Response(result.to_dict(), status=result.status_code)

