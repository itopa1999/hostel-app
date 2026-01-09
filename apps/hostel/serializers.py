from rest_framework import serializers
from apps.hostel.models import Floor, RoomType, Room


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
    
    class Meta:
        model = Room
        fields = ['id', 'floor', 'floor_number', 'room_type', 'room_type_name', 'number', 'status', 'price_override', 'notes', 'created_at', 'modified_at', 'is_deleted']
        read_only_fields = ['id', 'created_at', 'modified_at', 'is_deleted']
