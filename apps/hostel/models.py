from django.db import models
from utils.base_model import BaseModel
from utils.enums import RoomStatus, BookingStatus, PaymentMethod, PaymentStatus

class Hotel(BaseModel):
    name = models.CharField(max_length=255)
    id_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    address = models.TextField()
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    check_in_time = models.TimeField(default='14:00')
    check_out_time = models.TimeField(default='12:00')

    class Meta:
        verbose_name = "Hotel"
        verbose_name_plural = "Hotels"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.city})"
    

class Floor(BaseModel):
    number = models.PositiveIntegerField(unique=True)
    description = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = "Floor"
        verbose_name_plural = "Floors"
        ordering = ['number']

    def __str__(self):
        return f"Floor {self.number}"

    
class RoomType(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    max_occupancy = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    amenities = models.JSONField(default=list, blank=True, help_text="List of room amenities")

    class Meta:
        verbose_name = "Room Type"
        verbose_name_plural = "Room Types"
        ordering = ['name']

    def __str__(self):
        return f"{self.name}"
        

class Room(BaseModel):
    floor = models.ForeignKey(Floor, on_delete=models.SET_NULL, null=True, related_name='rooms')
    room_type = models.ForeignKey(RoomType, on_delete=models.PROTECT, related_name='rooms')
    number = models.CharField(max_length=10, unique=True)
    status = models.CharField(max_length=20, choices=RoomStatus.choices(), default=RoomStatus.AVAILABLE.value, db_index=True)
    price_override = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Override base price if set")
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = "Room"
        verbose_name_plural = "Rooms"
        ordering = ['number']
        indexes = [
            models.Index(fields=['status', '-created_at']),
        ]

    def __str__(self):
        return f"Room {self.number}"


class GuestProfile(BaseModel):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    nationality = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True, help_text="Guest preferences and notes")
    first_visit_date = models.DateField(null=True, blank=True)
    total_stays = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Guest Profile"
        verbose_name_plural = "Guest Profiles"
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Booking(BaseModel):
    guest = models.ForeignKey(GuestProfile, on_delete=models.CASCADE, related_name='bookings')
    room = models.ForeignKey(Room, on_delete=models.PROTECT, related_name='bookings')
    confirmation_code = models.CharField(max_length=50, unique=True, db_index=True)
    check_in = models.DateField()
    check_out = models.DateField()
    number_of_guests = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=BookingStatus.choices(), default=BookingStatus.RESERVED.value, db_index=True)
    payment_status = models.CharField(max_length=20, choices=PaymentStatus.choices(), default=PaymentStatus.PENDING.value)
    special_requests = models.TextField(blank=True)
    cancellation_date = models.DateTimeField(null=True, blank=True)
    cancellation_reason = models.TextField(blank=True)

    class Meta:
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['confirmation_code']),
            models.Index(fields=['guest', '-created_at']),
            models.Index(fields=['check_in', 'check_out']),
            models.Index(fields=['status', '-created_at']),
        ]

    def __str__(self):
        return f"Booking {self.confirmation_code} - {self.guest.name}"


class Invoice(BaseModel):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='invoice')
    invoice_number = models.CharField(max_length=50, unique=True, db_index=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, choices=PaymentStatus.choices(), default=PaymentStatus.PENDING.value)
    due_date = models.DateField(null=True, blank=True)
    payment_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = "Invoice"
        verbose_name_plural = "Invoices"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['invoice_number']),
            models.Index(fields=['payment_status', '-created_at']),
        ]

    def __str__(self):
        return f"Invoice {self.invoice_number}"


class Payment(BaseModel):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=PaymentMethod.choices())
    payment_status = models.CharField(max_length=20, choices=PaymentStatus.choices(), default=PaymentStatus.PENDING.value)
    transaction_id = models.CharField(max_length=100, unique=True, blank=True, null=True, db_index=True)
    receipt_number = models.CharField(max_length=100, blank=True)
    reference = models.CharField(max_length=100, blank=True)
    refund_date = models.DateTimeField(null=True, blank=True)
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['transaction_id']),
            models.Index(fields=['payment_status', '-created_at']),
        ]

    def __str__(self):
        return f"Payment {self.transaction_id or self.reference or self.id}"




