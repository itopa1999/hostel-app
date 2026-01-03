from rest_framework import serializers
from apps.users.models import User
from django.contrib.auth.models import Group


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating users"""
    
    groups = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Group.objects.all()
    )
    
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
            'groups',
        ]


class UserUpdateSerializer(serializers.Serializer):
    """Serializer for updating users (partial updates)"""
    username = serializers.CharField(required=False, allow_blank=False)
    email = serializers.EmailField(required=False, allow_blank=False)
    first_name = serializers.CharField(required=False, allow_blank=False)
    last_name = serializers.CharField(required=False, allow_blank=False)
    is_active = serializers.BooleanField(required=True)
    groups = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Group.objects.all(),
        required=False
    )


class ChangeUserPasswordSerializer(serializers.Serializer):
    """Serializer for changing user password"""
    
    new_password = serializers.CharField(required=True, write_only=True)
    user_id = serializers.IntegerField(required=True)