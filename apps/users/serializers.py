from rest_framework import serializers
from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    
    groups = serializers.StringRelatedField(many=True, read_only=True)
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'full_name',
            'id_number',
            'is_active',
            'is_staff',
            'is_superuser',
            'is_deleted',
            'groups',
        ]
        read_only_fields = [
            'id',
            'id_number',
            'created_at',
            'modified_at',
            'is_deleted',
        ]
    
    def get_full_name(self, obj):
        """Return full name of user"""
        return f"{obj.first_name} {obj.last_name}".strip()


class UserDetailSerializer(UserSerializer):
    """Extended serializer with additional user details"""
    
    user_permissions = serializers.StringRelatedField(many=True, read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    last_login = serializers.DateTimeField(read_only=True, allow_null=True)
    created_by = serializers.CharField(read_only=True, allow_null=True)
    modified_by = serializers.CharField(read_only=True, allow_null=True)
    deleted_by = serializers.CharField(read_only=True, allow_null=True)
    deleted_at = serializers.DateTimeField(read_only=True, allow_null=True)
    
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + [
            'user_permissions',
            'date_joined',
            'last_login',
            'created_by',
            'modified_by',
            'deleted_by',
            'deleted_at',
        ]        


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating users"""
    
    groups = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=__import__('django.contrib.auth.models', fromlist=['Group']).Group.objects.all(),
        required=False
    )
    
    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
            'is_active',
            'is_staff',
            'is_superuser',
            'password',
            'groups',
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'email': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
        }
    
    def update(self, instance, validated_data):
        """Update user with optional password hashing"""
        groups = validated_data.pop('groups', None)
        password = validated_data.pop('password', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)
        
        instance.save()
        
        if groups is not None:
            instance.groups.set(groups)
        
        return instance




class LoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    

class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for changing user password"""
    
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)