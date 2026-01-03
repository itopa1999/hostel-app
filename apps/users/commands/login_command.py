from django.conf import settings
from django.contrib.auth import authenticate
from urllib.parse import urlencode
from rest_framework_simplejwt.tokens import RefreshToken
from http import HTTPStatus

from utils.base_result import BaseResultWithData
from utils.log_helpers import OperationLogger
from apps.users.models import User


class LoginCommand:
    """Handle username/password login"""
    
    @staticmethod
    def Execute(username, password, request=None):
        """
        Authenticate user with username and password.
        
        Args:
            username (str): Username
            password (str): Password
                        
        Returns:
            BaseResultWithData: Result with tokens and user info
        """
        op = OperationLogger(
            "LoginCommand",
            username=username
        )
        op.start()
        
        # Authenticate user
        user = authenticate(username=username, password=password)
        
        if not user:
            op.fail(f"Invalid credentials for user {username}")
            return BaseResultWithData(
                message="Invalid username or password",
                status_code=HTTPStatus.UNAUTHORIZED
            )
        
        # Check if user is soft deleted
        if user.is_deleted:
            op.fail(f"User {username} has been deleted")
            return BaseResultWithData(
                message="User account not found",
                status_code=HTTPStatus.UNAUTHORIZED
            )
        
        if not user.is_active:
            op.fail(f"User {username} is inactive")
            return BaseResultWithData(
                message="User account is inactive",
                status_code=HTTPStatus.FORBIDDEN
            )
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        
        # Get group names
        group_names = ", ".join(user.groups.values_list("name", flat=True))
        
        op.success(f"Login successful for user {user.id}")
        
        return BaseResultWithData(
            message="Login successful",
            data={
                "access": access_token,
                "refresh": refresh_token,
                "email": user.email,
                "username": user.username,
                "name": f"{user.first_name} {user.last_name}",
                "id_number": user.id_number,
                "groups": group_names,
                "is_staff": user.is_staff,
                "is_superuser": user.is_superuser,
            },
            status_code=HTTPStatus.OK
        )
