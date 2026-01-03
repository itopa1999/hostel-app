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
    
    # @staticmethod
    # def Update(user_id, **kwargs):
    #     """
    #     Update user information.
        
    #     Args:
    #         user_id (int): User ID
    #         **kwargs: Fields to update (password and groups handled separately)
            
    #     Returns:
    #         BaseResultWithData: Result with updated user data
    #     """
    #     op = OperationLogger(
    #         "UserCommand.Update",
    #         user_id=user_id
    #     )
    #     op.start()
        
    #     try:
    #         user = User.objects.get(id=user_id, is_deleted=False)
            
    #         # Handle password separately
    #         password = kwargs.pop('password', None)
    #         groups = kwargs.pop('groups', None)
            
    #         # Update other fields
    #         for field, value in kwargs.items():
    #             if hasattr(user, field):
    #                 setattr(user, field, value)
            
    #         # Update password if provided
    #         if password:
    #             user.set_password(password)
            
    #         user.save()
            
    #         # Update groups if provided
    #         if groups:
    #             user.groups.set(groups)
            
    #         op.success(f"User {user_id} updated successfully")
    #         return BaseResultWithData(
    #             message="User updated successfully",
    #             data=UserSerializer(user).data,
    #             status_code=HTTPStatus.OK
    #         )
    #     except User.DoesNotExist:
    #         op.fail("User not found")
    #         return BaseResultWithData(
    #             message="User not found",
    #             status_code=HTTPStatus.NOT_FOUND
    #         )
    #     except Exception as e:
    #         op.fail(f"Error updating user: {str(e)}")
    #         return BaseResultWithData(
    #             message=str(e),
    #             status_code=HTTPStatus.INTERNAL_SERVER_ERROR
    #         )
    
    # @staticmethod
    # def Delete(user_id):
    #     """
    #     Delete user (soft or hard delete).
        
    #     Args:
    #         user_id (int): User ID
    #         soft_delete (bool): Soft delete (default) or hard delete
            
    #     Returns:
    #         BaseResultWithData: Result of deletion
    #     """
    #     op = OperationLogger(
    #         "UserCommand.Delete",
    #         user_id=user_id
    #     )
    #     op.start()
        
    #     try:
    #         user = User.objects.get(id=user_id, is_deleted=False)
    #         user.is_deleted = True
    #         user.save()
    #         op.success(f"User {user_id} soft deleted")
            
    #         return BaseResultWithData(
    #             message="User deleted successfully",
    #             status_code=HTTPStatus.OK
    #         )
    #     except User.DoesNotExist:
    #         op.fail("User not found")
    #         return BaseResultWithData(
    #             message="User not found",
    #             status_code=HTTPStatus.NOT_FOUND
    #         )
    
    # @staticmethod
    # def List(filters=None, page=1, per_page=20):
    #     """
    #     List users with optional filters and pagination.
        
    #     Args:
    #         filters (dict): Filter options - is_active, is_staff, group, search
    #         page (int): Page number (default 1)
    #         per_page (int): Results per page (default 20)
            
    #     Returns:
    #         BaseResultWithData: Result with paginated user list
    #     """
    #     op = OperationLogger("UserCommand.List")
    #     op.start()
        
    #     try:
    #         queryset = User.objects.filter(is_deleted=False)
            
    #         # Apply filters
    #         if filters:
    #             if 'is_active' in filters:
    #                 queryset = queryset.filter(is_active=filters['is_active'])
    #             if 'is_staff' in filters:
    #                 queryset = queryset.filter(is_staff=filters['is_staff'])
    #             if 'group' in filters:
    #                 queryset = queryset.filter(groups__name=filters['group'])
    #             if 'search' in filters:
    #                 queryset = queryset.filter(
    #                     Q(username__icontains=filters['search']) |
    #                     Q(email__icontains=filters['search']) |
    #                     Q(first_name__icontains=filters['search']) |
    #                     Q(last_name__icontains=filters['search'])
    #                 )
            
    #         # Pagination
    #         total = queryset.count()
    #         start = (page - 1) * per_page
    #         end = start + per_page
    #         users = queryset[start:end]
            
    #         op.success(f"Retrieved {len(users)} users")
    #         return BaseResultWithData(
    #             message="Users retrieved successfully",
    #             data={
    #                 "users": UserSerializer(users, many=True).data,
    #                 "total": total,
    #                 "page": page,
    #                 "per_page": per_page,
    #                 "total_pages": (total + per_page - 1) // per_page
    #             },
    #             status_code=HTTPStatus.OK
    #         )
    #     except Exception as e:
    #         op.fail(f"Error listing users: {str(e)}")
    #         return BaseResultWithData(
    #             message=str(e),
    #             status_code=HTTPStatus.INTERNAL_SERVER_ERROR
    #         )

