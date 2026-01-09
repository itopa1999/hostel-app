from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from apps.users.BBL.Commands.login_command import LoginCommand
from apps.users.BBL.Commands.user_command import UserCommand as UserCommand
from apps.users.BBL.Queries.user_command import UserCommand as UserQueryCommand
from apps.users.BBL.Queries.group_command import GroupQuery
from apps.users.serializers import ChangePasswordSerializer, LoginSerializer, UserDetailSerializer

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
        
        return Response(result.to_dict(), status=result.status_code)
    
class ChangePasswordViewAPI(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
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
        
        return Response(result.to_dict(), status=result.status_code)
    
    
class UserDetailViewAPI(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserDetailSerializer
    
    def get(self, request, *args, **kwargs):
        result = UserQueryCommand.Retrieve(user_id=self.request.user.id)
        return Response(result.to_dict(), status=result.status_code)


class GroupListAPIView(APIView):
    """List all groups with ID and name"""
    permission_classes = [AllowAny]
    authentication_classes = []
    
    def get(self, request):
        result = GroupQuery.ListAll()
        return Response(result.to_dict(), status=result.status_code)

