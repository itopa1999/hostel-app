from rest_framework import serializers
from apps.hostel.models import Hotel
from apps.users.models import User
from apps.administrator.models import Backup
from django.contrib.auth.models import Group
import uuid


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
    
    
class HotelSerializer(serializers.ModelSerializer):
    """Basic Hotel serializer for list view"""
    class Meta:
        model = Hotel
        fields = ('id', 'name', 'id_number', 'city', 'country', 'phone', 'email', 'created_at')
        read_only_fields = ('id', 'created_at')


class HotelDetailSerializer(serializers.ModelSerializer):
    """Detailed Hotel serializer with all fields"""
    class Meta:
        model = Hotel
        fields = (
            'id', 'name', 'id_number', 'address', 'city', 'country', 'postal_code',
            'phone', 'email', 'check_in_time', 'check_out_time',
            'created_at', 'modified_at', 'created_by', 'modified_by', 'is_deleted'
        )
        read_only_fields = ('id', 'created_at', 'modified_at', 'created_by', 'modified_by', 'is_deleted')


class HotelUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating a Hotel"""
    class Meta:
        model = Hotel
        fields = (
            'name', 'address', 'city', 'country', 'postal_code',
            'phone', 'email', 'check_in_time', 'check_out_time'
        )
    
    def validate_name(self, value):
        if value and len(value.strip()) == 0:
            raise serializers.ValidationError("Hotel name cannot be empty.")
        return value.strip() if value else value
    
    def validate_phone(self, value):
        if value and len(value.strip()) < 5:
            raise serializers.ValidationError("Phone number must be at least 5 characters.")
        return value


class BackupCreateSerializer(serializers.Serializer):
    """Serializer for creating a backup request"""
    start_date = serializers.DateField(required=True, help_text="Start date for backup range")
    end_date = serializers.DateField(required=True, help_text="End date for backup range")
    
    def validate(self, data):
        if data['end_date'] < data['start_date']:
            raise serializers.ValidationError("End date must be after start date.")
        return data


class BackupSerializer(serializers.ModelSerializer):
    """Serializer for backup records"""
    requested_by_username = serializers.CharField(
        source='requested_by.username',
        read_only=True
    )
    
    class Meta:
        model = Backup
        fields = [
            'id',
            'backup_name',
            'start_date',
            'end_date',
            'file_path',
            'file_size',
            'status',
            'record_count',
            'models_backed_up',
            'requested_by',
            'requested_by_username',
            'error_message',
            'created_at',
            'modified_at',
        ]
        read_only_fields = [
            'id',
            'file_path',
            'file_size',
            'record_count',
            'models_backed_up',
            'error_message',
            'created_at',
            'modified_at',
        ]
