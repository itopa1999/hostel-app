from rest_framework import serializers
from apps.hostel.models import Hotel, Floor, RoomType, Room, GuestProfile, Booking


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ['id', 'name', 'id_number', 'address', 'city', 'country', 'postal_code', 'phone', 'email', 'check_in_time', 'check_out_time', 'created_at', 'modified_at', 'is_deleted']
        read_only_fields = ['id', 'created_at', 'modified_at', 'is_deleted']


class FloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Floor
        fields = ['id', 'number', 'description', 'created_at', 'modified_at', 'is_deleted']
        read_only_fields = ['id', 'created_at', 'modified_at', 'is_deleted']


class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = ['id', 'name', 'base_price', 'max_occupancy', 'description', 'amenities', 'created_at', 'modified_at', 'is_deleted']
        read_only_fields = ['id', 'created_at', 'modified_at', 'is_deleted']


class RoomSerializer(serializers.ModelSerializer):
    floor_number = serializers.CharField(source='floor.number', read_only=True)
    room_type_name = serializers.CharField(source='room_type.name', read_only=True)
    max_occupancy = serializers.IntegerField(source='room_type.max_occupancy', read_only=True)
    base_price = serializers.DecimalField(source='room_type.base_price', max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = Room
        fields = ['id', 'floor', 'floor_number', 'room_type', 'room_type_name', 'max_occupancy', 'base_price', 'number', 'status', 'price_override', 'notes', 'created_at', 'modified_at', 'is_deleted']
        read_only_fields = ['id', 'created_at', 'modified_at', 'is_deleted']


class GuestProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuestProfile
        fields = ['id', 'name', 'email', 'phone', 'address', 'city', 'country', 'postal_code', 'nationality', 'notes', 'first_visit_date', 'total_stays', 'created_at', 'modified_at', 'is_deleted']
        read_only_fields = ['id', 'created_at', 'modified_at', 'is_deleted']


class BookingSerializer(serializers.ModelSerializer):
    guest_name = serializers.CharField(source='guest.name', read_only=True)
    room_number = serializers.CharField(source='room.number', read_only=True)
    room_type_name = serializers.CharField(source='room.room_type.name', read_only=True)
    
    class Meta:
        model = Booking
        fields = ['id', 'guest', 'guest_name', 'room', 'room_number', 'room_type_name', 'confirmation_code', 'check_in', 'check_out', 'number_of_guests', 'status', 'payment_status', 'special_requests', 'cancellation_date', 'cancellation_reason', 'created_at', 'modified_at', 'is_deleted']
        read_only_fields = ['id', 'confirmation_code', 'created_at', 'modified_at', 'is_deleted']