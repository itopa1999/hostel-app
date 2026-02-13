from http import HTTPStatus
from utils.base_result import BaseResultWithData
from utils.log_helpers import OperationLogger
from apps.users.models import User
from apps.users.serializers import UserDetailSerializer
from utils.audit.audit_logger import AuditLogger


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
    
    @staticmethod
    def List():
        """
        List all users (non-deleted) with their groups and details.
        
        Returns:
            BaseResultWithData: Result with list of users
        """
        op = OperationLogger("UserCommand.List")
        op.start()
        
        try:
            users = User.objects.filter(is_superuser=False).all()
            serializer = UserDetailSerializer(users, many=True)
            op.success(f"Retrieved {users.count()} users")
            return BaseResultWithData(
                message="Users retrieved successfully",
                data=serializer.data,
                status_code=HTTPStatus.OK
            )
        except Exception as e:
            op.fail(f"Failed to retrieve users: {str(e)}", exc=e)
            AuditLogger.log_failure(
                'LIST_USERS',
                'User',
                description=f"Failed to list users - {str(e)}"
            )
            return BaseResultWithData(
                message=str(e),
                status_code=HTTPStatus.BAD_REQUEST
            )
