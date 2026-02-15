from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from apps.users.BBL.Commands.login_command import LoginCommand
from apps.users.BBL.Commands.user_command import UserCommand as UserCommand
from apps.users.BBL.Queries.user_command import UserCommand as UserQueryCommand
from apps.users.BBL.Queries.group_command import GroupQuery
from apps.users.serializers import ChangePasswordSerializer, LoginSerializer, UserDetailSerializer, UserUpdateSerializer
from utils.permissions import IsAdminPermission, IsAuthenticatedAndNotDeleted

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView


User = get_user_model()


class LoginViewAPI(generics.GenericAPIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = LoginSerializer
    
    def post(self, request, *args, **kwargs):
        
        result = LoginCommand.Execute(
            username=request.data.get('username'),
            password=request.data.get('password'),
            group_id=request.data.get('group_id'),
            request=request
        )
        
        return Response(result.to_dict(), status=result.status_code.value)
    
class ChangePasswordViewAPI(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedAndNotDeleted]
    serializer_class = ChangePasswordSerializer
    
    def post(self, request, *args, **kwargs):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        
        result = UserCommand.changePassword(
            user_id=user.id,
            old_password=old_password,
            new_password=new_password,
            performed_by=user
        )
        
        return Response(result.to_dict(), status=result.status_code.value)
    
    
class UserDetailViewAPI(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedAndNotDeleted]
    serializer_class = UserDetailSerializer
    
    def get(self, request, *args, **kwargs):
        result = UserQueryCommand.Retrieve(user_id=self.request.user.id)
        return Response(result.to_dict(), status=result.status_code.value)


class UpdateUserViewAPI(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedAndNotDeleted]
    serializer_class = UserUpdateSerializer
    
    def put(self, request, user_id=None, *args, **kwargs):
        target_user_id = request.user.id
        
        email = request.data.get('email')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        
        result = UserCommand.Update(
            user_id=target_user_id,
            email=email,
            first_name=first_name,
            last_name=last_name,
            performed_by=request.user
        )
        
        return Response(result.to_dict(), status=result.status_code.value)


class GroupListAPIView(APIView):
    """List all groups with ID and name"""
    permission_classes = [AllowAny]
    authentication_classes = []
    
    def get(self, request):
        result = GroupQuery.ListAll()
        return Response(result.to_dict(), status=result.status_code.value)


class UserListAPIView(generics.GenericAPIView):
    """List all users with groups and details"""
    permission_classes = [IsAuthenticatedAndNotDeleted, IsAdminPermission]
    
    def get(self, request):
        result = UserQueryCommand.List()
        return Response(result.to_dict(), status=result.status_code.value)


class UserDeleteAPIView(generics.GenericAPIView):
    """Soft delete or restore a user"""
    permission_classes = [IsAuthenticatedAndNotDeleted, IsAdminPermission]
    
    def post(self, request, user_id):
        result = UserCommand.ToggleDelete(user_id=user_id, performed_by=request.user)
        return Response(result.to_dict(), status=result.status_code.value)


class UserUpdateGroupsAPIView(generics.GenericAPIView):
    """Update user's groups and optionally password"""
    permission_classes = [IsAuthenticatedAndNotDeleted, IsAdminPermission]
    
    def post(self, request, user_id):
        group_ids = request.data.get('groups', [])
        password = request.data.get('password', None)
        result = UserCommand.UpdateGroups(user_id=user_id, group_ids=group_ids, password=password, performed_by=request.user)
        return Response(result.to_dict(), status=result.status_code.value)


class UserCreateAPIView(APIView):
    """Create new user"""
    permission_classes = [IsAuthenticatedAndNotDeleted, IsAdminPermission]
    
    def post(self, request):
        result = UserCommand.Create(request.data, performed_by=request.user)
        return Response(result.to_dict(), status=result.status_code.value)
