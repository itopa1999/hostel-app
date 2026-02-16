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
    """
    Permission class to ensure user has Admin role AND selected Admin during login.
    Checks the 'user_group' cookie set during login to enforce selected role only.
    """
    message = "Access is not granted. Admin role required."
    
    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        if user.is_deleted:
            return False

        # Check if user has Admin group
        if not user.groups.filter(name=GroupNames.ADMIN.value).exists():
            return False

        # Check if user SELECTED Admin role during login
        selected_role = request.COOKIES.get('user_group', '').lower()
        
        print(f"User '{user.username}' has groups: {[g.name for g in user.groups.all()]}, selected role: '{selected_role}'")
        
        if selected_role != GroupNames.ADMIN.value.lower():
            return False

        return True


class IsStaffPermission(BasePermission):
    """
    Permission class to ensure user has Staff role AND selected Staff during login.
    Checks the 'user_group' cookie set during login to enforce selected role only.
    """
    message = "Access is not granted. Staff role required."
    
    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        if user.is_deleted:
            return False

        # Check if user has Staff group
        if not user.groups.filter(name=GroupNames.STAFF.value).exists():
            return False

        # Check if user SELECTED Staff role during login
        selected_role = request.COOKIES.get('user_group', '').lower()
        if selected_role != GroupNames.STAFF.value.lower():
            return False

        return True


class HasActiveGroupPermission(BasePermission):
    """
    Permission class to ensure user has at least one active group.
    This is the base permission that allows any authenticated user with groups.
    """
    message = "User has no active groups assigned."
    
    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        if user.is_deleted:
            return False

        # Check if user has at least one group
        if not user.groups.exists():
            return False

        return True


class IsAdminOrReadOnly(BasePermission):
    """
    Permission class where only selected Admin role can create/update/delete, others can only read.
    Enforces that user SELECTED Admin during login, not just has Admin group.
    """
    message = "Access is not granted. Admin role required for this action."
    
    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        if user.is_deleted:
            return False

        # Allow read-only methods for all authenticated users
        if request.method in permissions.SAFE_METHODS:
            return True

        # Restrict write methods to users who SELECTED Admin during login
        selected_role = request.COOKIES.get('user_group', '').lower()
        has_admin_group = user.groups.filter(name=GroupNames.ADMIN.value).exists()
        
        return has_admin_group and selected_role == GroupNames.ADMIN.value.lower()


class IsStaffOrReadOnly(BasePermission):
    """
    Permission class where Staff+ (users who selected Staff or Admin) can create/update/delete.
    Others can only read. Enforces SELECTED role during login.
    """
    message = "Access is not granted. Staff or Admin role required for this action."
    
    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        if user.is_deleted:
            return False

        # Allow read-only methods for all authenticated users
        if request.method in permissions.SAFE_METHODS:
            return True

        # Restrict write methods to users who SELECTED Staff or Admin during login
        selected_role = request.COOKIES.get('user_group', '').lower()
        allowed_groups = [GroupNames.STAFF.value.lower(), GroupNames.ADMIN.value.lower()]
        has_required_group = user.groups.filter(
            name__in=[GroupNames.STAFF.value, GroupNames.ADMIN.value]
        ).exists()
        
        return has_required_group and selected_role in allowed_groups
