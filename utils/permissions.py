# third party imports
from rest_framework import permissions
from rest_framework.permissions import BasePermission

from utils.enums import GroupNames


class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to allow users to edit their own object.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user


class IsAuthenticatedAndNotDeleted(BasePermission):
    """
    Custom permission to ensure user is authenticated and not deleted.
    """
    message = "Access is not granted."
    
    def has_permission(self, request, view):
        user = request.user
        
        if not user.is_authenticated:
            return False
        
        if user.is_deleted:
            return False
        
        return True


class IsAdminPermission(BasePermission):
    message = "Access is not granted."
    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        if user.is_deleted:
            return False

        if not user.groups.filter(name=GroupNames.ADMIN.value).exists():
            return False

        return True