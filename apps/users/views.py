from django.contrib.auth import get_user_model


from apps.users.BBL.Commands.login_command import LoginCommand
from apps.users.BBL.Commands.user_command import UserCommand as UserCommand
from apps.users.BBL.Queries.user_command import UserCommand as UserQueryCommand
from apps.users.serializers import ChangePasswordSerializer, LoginSerializer, UserCreateSerializer, UserDetailSerializer

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics

from utils.permissions import IsAdminPermission


User = get_user_model()


class LoginViewAPI(generics.GenericAPIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = LoginSerializer
    
    def post(self, request, *args, **kwargs):
        
        result = LoginCommand.Execute(
            username=request.data.get('username'),
            password=request.data.get('password'),
            request=request
        )
        
        return Response(result.to_dict(), status=result.status_code)
        
        
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
        )
        
        return Response(result.to_dict(), status=result.status_code)
    
    
class UserDetailViewAPI(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserDetailSerializer
    
    def get(self, request, *args, **kwargs):
        result = UserQueryCommand.Retrieve(user_id=self.request.user.id)
        return Response(result.to_dict(), status=result.status_code)


