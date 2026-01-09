from rest_framework import serializers
from apps.hostel.models import Hotel, Floor, RoomType, Room, GuestProfile, Booking, Invoice, Payment


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


class HotelCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new Hotel"""
    class Meta:
        model = Hotel
        fields = (
            'name', 'address', 'city', 'country', 'postal_code',
            'phone', 'email', 'check_in_time', 'check_out_time'
        )
    
    def validate_name(self, value):
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError("Hotel name cannot be empty.")
        return value.strip()
    
    def validate_phone(self, value):
        if not value or len(value.strip()) < 5:
            raise serializers.ValidationError("Phone number must be at least 5 characters.")
        return value
    
    def validate_email(self, value):
        if Hotel.objects.filter(email=value, is_deleted=False).exists():
            raise serializers.ValidationError("Hotel with this email already exists.")
        return value


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
