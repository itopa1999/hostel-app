from django.contrib import admin
from django.utils.html import format_html
from apps.hostel.models import Hotel, Floor, RoomType, Room, GuestProfile, Booking, Invoice, Payment


# Inline Admins for Hotel
class FloorInline(admin.TabularInline):
    model = Floor
    extra = 1
    fields = ('number', 'description')


class RoomTypeInline(admin.TabularInline):
    model = RoomType
    extra = 1
    fields = ('name', 'base_price', 'max_occupancy')


class RoomInline(admin.TabularInline):
    model = Room
    extra = 1
    fields = ('floor', 'number', 'room_type', 'status', 'price_override')
    readonly_fields = ('created_at',)


# Hotel Admin
@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    """Hotel admin with inline management of floors and room types"""
    list_display = ('name', 'id_number', 'city_country', 'phone', 'email', 'created_at')
    list_display_links = ('name', 'id_number')
    search_fields = ('name', 'id_number', 'city', 'country', 'email')
    list_filter = ('city', 'country', 'created_at')
    readonly_fields = ('created_at', 'modified_at', 'created_by', 'modified_by', 'deleted_at', 'deleted_by')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    list_per_page = 20
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'id_number', 'email', 'phone')
        }),
        ('Address', {
            'fields': ('address', 'city', 'country', 'postal_code')
        }),
        ('Check-in/out Times', {
            'fields': ('check_in_time', 'check_out_time')
        }),
        ('Base Model Info', {
            'fields': ('created_at', 'modified_at', 'created_by', 'modified_by', 'is_deleted', 'deleted_at', 'deleted_by'),
            'classes': ('collapse',)
        }),
    )
    
    def city_country(self, obj):
        return f"{obj.city}, {obj.country}"
    city_country.short_description = "Location"


# Floor Admin
@admin.register(Floor)
class FloorAdmin(admin.ModelAdmin):
    list_display = ('number', 'description', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('number', 'description')
    readonly_fields = ('created_at', 'modified_at', 'created_by', 'modified_by')
    ordering = ('number',)
    list_per_page = 30
    
    fieldsets = (
        ('Floor Information', {
            'fields': ('number', 'description')
        }),
        ('Base Model Info', {
            'fields': ('created_at', 'modified_at', 'created_by', 'modified_by', 'is_deleted', 'deleted_at', 'deleted_by'),
            'classes': ('collapse',)
        }),
    )


# Room Type Admin
@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_price', 'max_occupancy', 'created_at')
    list_filter = ('max_occupancy', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'modified_at', 'created_by', 'modified_by')
    ordering = ('name',)
    list_per_page = 25
    
    fieldsets = (
        ('Room Type Information', {
            'fields': ('name', 'description')
        }),
        ('Pricing & Occupancy', {
            'fields': ('base_price', 'max_occupancy')
        }),
        ('Amenities', {
            'fields': ('amenities',)
        }),
        ('Base Model Info', {
            'fields': ('created_at', 'modified_at', 'created_by', 'modified_by', 'is_deleted', 'deleted_at', 'deleted_by'),
            'classes': ('collapse',)
        }),
    )


# Room Admin
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'floor', 'room_type', 'status_display', 'price_display', 'created_at')
    list_display_links = ('room_number',)
    list_filter = ('status', 'room_type', 'floor', 'created_at')
    search_fields = ('number', 'notes')
    readonly_fields = ('created_at', 'modified_at', 'created_by', 'modified_by')
    ordering = ('number',)
    date_hierarchy = 'created_at'
    list_per_page = 50
    
    fieldsets = (
        ('Room Information', {
            'fields': ('floor', 'number', 'room_type')
        }),
        ('Pricing', {
            'fields': ('price_override',)
        }),
        ('Status & Notes', {
            'fields': ('status', 'notes')
        }),
        ('Base Model Info', {
            'fields': ('created_at', 'modified_at', 'created_by', 'modified_by', 'is_deleted', 'deleted_at', 'deleted_by'),
            'classes': ('collapse',)
        }),
    )
    
    def room_number(self, obj):
        return f"Room {obj.number}"
    room_number.short_description = "Room"
    
    def status_display(self, obj):
        colors = {
            'AVAILABLE': 'green',
            'OCCUPIED': 'orange',
            'DIRTY': 'red',
            'MAINTENANCE': 'blue',
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="color: {};">●</span> {}',
            color,
            obj.get_status_display()
        )
    status_display.short_description = "Status"
    
    def price_display(self, obj):
        if obj.price_override:
            return format_html('<span style="font-weight: bold;">${}</span> (Override)', obj.price_override)
        return f"${obj.room_type.base_price}"
    price_display.short_description = "Price"


# Guest Profile Admin
@admin.register(GuestProfile)
class GuestProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'country', 'total_stays', 'created_at')
    list_display_links = ('name', 'email')
    search_fields = ('name', 'email', 'phone', 'city')
    list_filter = ('country', 'created_at', 'total_stays')
    readonly_fields = ('created_at', 'modified_at', 'created_by', 'modified_by', 'total_stays')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    list_per_page = 30
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'email', 'phone', 'nationality')
        }),
        ('Address', {
            'fields': ('address', 'city', 'country', 'postal_code')
        }),
        ('Guest History', {
            'fields': ('first_visit_date', 'total_stays', 'notes')
        }),
        ('Base Model Info', {
            'fields': ('created_at', 'modified_at', 'created_by', 'modified_by', 'is_deleted', 'deleted_at', 'deleted_by'),
            'classes': ('collapse',)
        }),
    )


# Booking Admin
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('confirmation_code', 'guest_name', 'room_display', 'check_in', 'check_out', 'status_display', 'payment_display', 'created_at')
    list_display_links = ('confirmation_code', 'guest_name')
    search_fields = ('confirmation_code', 'guest__name', 'room__number')
    list_filter = ('status', 'payment_status', 'check_in', 'check_out', 'created_at')
    readonly_fields = ('created_at', 'modified_at', 'created_by', 'modified_by', 'confirmation_code')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    list_per_page = 25
    
    fieldsets = (
        ('Booking Information', {
            'fields': ('confirmation_code', 'guest', 'room', 'number_of_guests')
        }),
        ('Dates', {
            'fields': ('check_in', 'check_out')
        }),
        ('Status', {
            'fields': ('status', 'payment_status')
        }),
        ('Special Requests & Notes', {
            'fields': ('special_requests',)
        }),
        ('Cancellation', {
            'fields': ('cancellation_date', 'cancellation_reason'),
            'classes': ('collapse',)
        }),
        ('Base Model Info', {
            'fields': ('created_at', 'modified_at', 'created_by', 'modified_by', 'is_deleted', 'deleted_at', 'deleted_by'),
            'classes': ('collapse',)
        }),
    )
    
    def guest_name(self, obj):
        return obj.guest.name
    guest_name.short_description = "Guest"
    
    def room_display(self, obj):
        return f"{obj.room.hotel.name} - Room {obj.room.number}"
    room_display.short_description = "Room"
    
    def status_display(self, obj):
        colors = {
            'RESERVED': 'blue',
            'CHECKED_IN': 'green',
            'CHECKED_OUT': 'gray',
            'CANCELLED': 'red',
            'NO_SHOW': 'orange',
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="color: {};">●</span> {}',
            color,
            obj.get_status_display()
        )
    status_display.short_description = "Booking Status"
    
    def payment_display(self, obj):
        colors = {
            'PENDING': 'orange',
            'COMPLETED': 'green',
            'FAILED': 'red',
            'REFUNDED': 'blue',
        }
        color = colors.get(obj.payment_status, 'gray')
        return format_html(
            '<span style="color: {};">●</span> {}',
            color,
            obj.get_payment_status_display()
        )
    payment_display.short_description = "Payment Status"


# Invoice Admin
@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'booking_display', 'total_display', 'payment_status_display', 'due_date', 'created_at')
    list_display_links = ('invoice_number', 'booking_display')
    search_fields = ('invoice_number', 'booking__confirmation_code', 'booking__guest__name')
    list_filter = ('payment_status', 'created_at', 'due_date')
    readonly_fields = ('created_at', 'modified_at', 'created_by', 'modified_by', 'invoice_number')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    list_per_page = 25
    
    fieldsets = (
        ('Invoice Information', {
            'fields': ('invoice_number', 'booking')
        }),
        ('Financial Summary', {
            'fields': ('subtotal', 'discount_amount', 'tax', 'total')
        }),
        ('Dates & Payment', {
            'fields': ('due_date', 'payment_date', 'payment_status')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Base Model Info', {
            'fields': ('created_at', 'modified_at', 'created_by', 'modified_by', 'is_deleted', 'deleted_at', 'deleted_by'),
            'classes': ('collapse',)
        }),
    )
    
    def booking_display(self, obj):
        return f"{obj.booking.confirmation_code} - {obj.booking.guest.name}"
    booking_display.short_description = "Booking"
    
    def total_display(self, obj):
        return format_html('<span style="font-weight: bold; color: green;">${}</span>', obj.total)
    total_display.short_description = "Total"
    
    def payment_status_display(self, obj):
        colors = {
            'PENDING': 'orange',
            'COMPLETED': 'green',
            'FAILED': 'red',
            'REFUNDED': 'blue',
        }
        color = colors.get(obj.payment_status, 'gray')
        return format_html(
            '<span style="color: {};">●</span> {}',
            color,
            obj.get_payment_status_display()
        )
    payment_status_display.short_description = "Payment Status"


# Payment Admin
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('transaction_id_display', 'invoice_display', 'amount_display', 'method_display', 'payment_status_display', 'created_at')
    list_display_links = ('transaction_id_display', 'invoice_display')
    search_fields = ('transaction_id', 'receipt_number', 'reference', 'invoice__invoice_number')
    list_filter = ('method', 'payment_status', 'created_at')
    readonly_fields = ('created_at', 'modified_at', 'created_by', 'modified_by')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    list_per_page = 30
    
    fieldsets = (
        ('Payment Information', {
            'fields': ('invoice', 'amount', 'method')
        }),
        ('Payment Details', {
            'fields': ('payment_status', 'transaction_id', 'receipt_number', 'reference')
        }),
        ('Refund Information', {
            'fields': ('refund_date', 'refund_amount'),
            'classes': ('collapse',)
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Base Model Info', {
            'fields': ('created_at', 'modified_at', 'created_by', 'modified_by', 'is_deleted', 'deleted_at', 'deleted_by'),
            'classes': ('collapse',)
        }),
    )
    
    def transaction_id_display(self, obj):
        return obj.transaction_id or format_html('<span style="color: gray;">N/A</span>')
    transaction_id_display.short_description = "Transaction ID"
    
    def invoice_display(self, obj):
        return obj.invoice.invoice_number
    invoice_display.short_description = "Invoice"
    
    def amount_display(self, obj):
        return format_html('<span style="font-weight: bold; color: green;">${}</span>', obj.amount)
    amount_display.short_description = "Amount"
    
    def method_display(self, obj):
        colors = {
            'CASH': 'green',
            'CARD': 'blue',
            'TRANSFER': 'orange',
        }
        color = colors.get(obj.method, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 6px; border-radius: 3px;">{}</span>',
            color,
            obj.get_method_display()
        )
    method_display.short_description = "Method"
    
    def payment_status_display(self, obj):
        colors = {
            'PENDING': 'orange',
            'COMPLETED': 'green',
            'FAILED': 'red',
            'REFUNDED': 'blue',
        }
        color = colors.get(obj.payment_status, 'gray')
        return format_html(
            '<span style="color: {};">●</span> {}',
            color,
            obj.get_payment_status_display()
        )
    payment_status_display.short_description = "Status"
