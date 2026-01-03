from http import HTTPStatus
from utils.base_result import BaseResultWithData
from utils.log_helpers import OperationLogger
from apps.users.models import User
from apps.users.serializers import UserDetailSerializer


class UserCommand:
    """Handle CRUD operations for User"""
            
    @staticmethod
    def Retrieve(user_id):
        """
        Retrieve user details by ID.
        
        Args:
            user_id (int): User ID
            
        Returns:
            BaseResultWithData: Result with user details
        """
        
        try:
            user = User.objects.get(id=user_id, is_deleted=False)
            return BaseResultWithData(
                message="User retrieved successfully",
                data=UserDetailSerializer(user).data,
                status_code=HTTPStatus.OK
            )
        except User.DoesNotExist:
            return BaseResultWithData(
                message="User not found",
                status_code=HTTPStatus.NOT_FOUND
            )
    
