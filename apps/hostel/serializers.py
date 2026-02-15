from rest_framework import serializers
from apps.hostel.models import Hotel, Floor, RoomType, Room, GuestProfile, Booking, Invoice, Payment, Setting


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
    
    def update(self, instance, validated_data):
        """Prevent updating room if it's in occupied status"""
        from utils.enums import RoomStatus
        
        if instance.status == RoomStatus.OCCUPIED.value:
            raise serializers.ValidationError(
                "Cannot update room while it is in occupied status. Please change the room status first."
            )
        
        return super().update(instance, validated_data)


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


class InvoiceSerializer(serializers.ModelSerializer):
    booking_confirmation = serializers.CharField(source='booking.confirmation_code', read_only=True)
    guest_name = serializers.CharField(source='booking.guest.name', read_only=True)
    check_in = serializers.DateField(source='booking.check_in', read_only=True)
    check_out = serializers.DateField(source='booking.check_out', read_only=True)
    nights = serializers.SerializerMethodField()
    room = serializers.CharField(source='booking.room.number', read_only=True)
    room_type = serializers.CharField(source='booking.room.room_type.name', read_only=True)
    number_of_guests = serializers.IntegerField(source='booking.number_of_guests', read_only=True)
    
    def get_nights(self, obj):
        """Calculate number of nights from booking check_in and check_out dates"""
        if obj.booking and obj.booking.check_in and obj.booking.check_out:
            nights = (obj.booking.check_out - obj.booking.check_in).days
            return nights if nights > 0 else 1
        return 1
    
    class Meta:
        model = Invoice
        fields = ['id', 'booking', 'booking_confirmation', 'guest_name', 'room', 'room_type', 'number_of_guests', 'check_in', 'check_out', 'nights', 'invoice_number', 'subtotal', 'discount_amount', 'tax', 'total', 'payment_status', 'due_date', 'payment_date', 'notes', 'created_at', 'modified_at', 'is_deleted']
        read_only_fields = ['id', 'invoice_number', 'created_at', 'modified_at', 'is_deleted']


class PaymentSerializer(serializers.ModelSerializer):
    invoice_number = serializers.CharField(source='invoice.invoice_number', read_only=True)
    booking_confirmation = serializers.CharField(source='invoice.booking.confirmation_code', read_only=True)
    
    class Meta:
        model = Payment
        fields = ['id', 'invoice', 'invoice_number', 'booking_confirmation', 'amount', 'method', 'payment_status', 'transaction_id', 'receipt_number', 'reference', 'refund_date', 'refund_amount', 'notes', 'created_at', 'modified_at', 'is_deleted']
        read_only_fields = ['id', 'created_at', 'modified_at', 'is_deleted']


class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = ['id', 'tax_percentage', 'default_discount_percentage', 'description', 'created_at', 'modified_at', 'is_deleted']
        read_only_fields = ['id', 'created_at', 'modified_at', 'is_deleted']