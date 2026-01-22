import uuid
from http import HTTPStatus
from apps.hostel.models import Booking, GuestProfile
from apps.hostel.serializers import BookingSerializer
from utils.base_result import BaseResultWithData
from utils.log_helpers import OperationLogger
from utils.audit.audit_logger import AuditLogger
from utils.serialization_helpers import serialize_for_audit


class BookingCommand:
    
    @staticmethod
    def Create(data, user=None):
        op = OperationLogger("BookingCommand.Create", guest_id=data.get('guest'), room_id=data.get('room'))
        op.start()
        
        # Check if guest is deleted
        if 'guest' in data:
            try:
                guest = GuestProfile.objects.get(id=data['guest'])
                if guest.is_deleted:
                    op.fail(f"Guest with id {data['guest']} is deleted")
                    return BaseResultWithData(
                        data=None,
                        status_code=HTTPStatus.BAD_REQUEST,
                        message="The selected guest is deleted. Please select another guest or restore the deleted one"
                    )
            except GuestProfile.DoesNotExist:
                op.fail(f"Guest with id {data['guest']} not found")
                return BaseResultWithData(
                    data=None,
                    status_code=HTTPStatus.NOT_FOUND,
                    message="Guest not found"
                )
        
        # Check if room and its floor are deleted
        if 'room' in data:
            from apps.hostel.models import Room
            from utils.enums import RoomStatus
            try:
                room = Room.objects.get(id=data['room'])
                if room.is_deleted:
                    op.fail(f"Room with id {data['room']} is deleted")
                    return BaseResultWithData(
                        data=None,
                        status_code=HTTPStatus.BAD_REQUEST,
                        message="The selected room is deleted. Please select another room or restore the deleted one"
                    )
                if room.floor and room.floor.is_deleted:
                    op.fail(f"Floor with id {room.floor.id} is deleted")
                    return BaseResultWithData(
                        data=None,
                        status_code=HTTPStatus.BAD_REQUEST,
                        message="The floor of the selected room is deleted. Please select a room from a non-deleted floor or restore the deleted floor"
                    )
                if room.status != RoomStatus.AVAILABLE.value:
                    op.fail(f"Room with id {data['room']} is not available")
                    return BaseResultWithData(
                        data=None,
                        status_code=HTTPStatus.BAD_REQUEST,
                        message=f"The selected room is not available (current status: {room.status}). Please select another available room"
                    )
                # Check if number of guests exceeds room occupancy
                number_of_guests = data.get('number_of_guests', 1)
                if number_of_guests > room.room_type.max_occupancy:
                    op.fail(f"Number of guests ({number_of_guests}) exceeds room max occupancy ({room.room_type.max_occupancy})")
                    return BaseResultWithData(
                        data=None,
                        status_code=HTTPStatus.BAD_REQUEST,
                        message=f"The number of guests ({number_of_guests}) exceeds the room's maximum occupancy ({room.room_type.max_occupancy}). Please select a larger room or reduce the number of guests"
                    )
            except Room.DoesNotExist:
                op.fail(f"Room with id {data['room']} not found")
                return BaseResultWithData(
                    data=None,
                    status_code=HTTPStatus.NOT_FOUND,
                    message="Room not found"
                )
        
        # Generate confirmation code if not provided
        if 'confirmation_code' not in data or not data.get('confirmation_code'):
            # Get the last booking confirmation code and increment
            last_booking = Booking.objects.all().order_by('-id').first()
            if last_booking and last_booking.confirmation_code:
                try:
                    # Extract number from confirmation code (BK-0001 -> 1)
                    code_number = int(last_booking.confirmation_code.split('-')[-1])
                    next_number = code_number + 1
                except (ValueError, IndexError):
                    next_number = 1
            else:
                next_number = 1
            
            data['confirmation_code'] = f"BK-{next_number:04d}"
        
        # Validate booking status - disabled statuses on creation
        if 'status' in data:
            from utils.enums import BookingStatus
            disabled_statuses = [BookingStatus.CANCELLED.value, BookingStatus.NO_SHOW.value, BookingStatus.CHECKED_OUT.value]
            if data['status'] in disabled_statuses:
                op.fail(f"Status {data['status']} cannot be set when creating a new booking")
                return BaseResultWithData(
                    data=None,
                    status_code=HTTPStatus.BAD_REQUEST,
                    message=f"Status '{data['status']}' is not allowed when creating a new booking. You can only use RESERVED or CHECKED_IN"
                )
        
        # Validate check-in and check-out dates
        from django.utils import timezone
        from django.utils.dateparse import parse_date
        
        if 'check_in' in data and data['check_in']:
            check_in_date = parse_date(data['check_in']) if isinstance(data['check_in'], str) else data['check_in']
            if check_in_date and check_in_date < timezone.now().date():
                op.fail("Check-in date must be today or in the future")
                return BaseResultWithData(
                    data=None,
                    status_code=HTTPStatus.BAD_REQUEST,
                    message="Check-in date must be today or in the future"
                )
        
        if 'check_in' in data and 'check_out' in data and data['check_in'] and data['check_out']:
            check_in_date = parse_date(data['check_in']) if isinstance(data['check_in'], str) else data['check_in']
            check_out_date = parse_date(data['check_out']) if isinstance(data['check_out'], str) else data['check_out']
            if check_in_date and check_out_date and check_out_date < check_in_date:
                op.fail("Check-out date must be same or after check-in date")
                return BaseResultWithData(
                    data=None,
                    status_code=HTTPStatus.BAD_REQUEST,
                    message="Check-out date must be same or after check-in date"
                )
        
        serializer = BookingSerializer(data=data)
        if not serializer.is_valid():
            op.fail(f"Validation failed: {serializer.errors}")
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.BAD_REQUEST,
                message=f"Validation failed: {serializer.errors}"
            )
        
        try:
            validated_data = serializer.validated_data
            
            # Ensure confirmation_code is set and not empty
            if not validated_data.get('confirmation_code'):
                # Get the last booking confirmation code and increment
                last_booking = Booking.objects.all().order_by('-id').first()
                if last_booking and last_booking.confirmation_code:
                    try:
                        # Extract number from confirmation code (BK-0001 -> 1)
                        code_number = int(last_booking.confirmation_code.split('-')[-1])
                        next_number = code_number + 1
                    except (ValueError, IndexError):
                        next_number = 1
                else:
                    next_number = 1
                
                validated_data['confirmation_code'] = f"BK-{next_number:04d}"
            
            booking = Booking.objects.create(**validated_data)
            
            # Update GuestProfile - set first_visit_date and increment total_stays
            guest = booking.guest
            if not guest.first_visit_date:
                guest.first_visit_date = booking.check_in
            guest.total_stays += 1
            guest.save()
            
            # Automatically create invoice for the booking
            from apps.hostel.models import Invoice, Setting
            from datetime import timedelta
            
            try:
                # Calculate number of nights for the booking
                nights = (booking.check_out - booking.check_in).days
                if nights == 0:
                    nights = 1
                
                room_price = booking.room.get_price()
                subtotal = room_price * nights
                
                # Get settings for tax and discount
                try:
                    settings = Setting.get_settings()
                    tax_percentage = settings.tax_percentage if settings else 0
                    discount_percentage = settings.default_discount_percentage if settings else 0
                except Exception as settings_error:
                    op.fail(f"Failed to get settings: {str(settings_error)}")
                    tax_percentage = 0
                    discount_percentage = 0
                
                # Calculate discount and tax amounts
                discount_amount = (subtotal * discount_percentage) / 100
                tax_amount = ((subtotal - discount_amount) * tax_percentage) / 100
                total = subtotal - discount_amount + tax_amount
                
                # Generate invoice number (INV-0001)
                last_invoice = Invoice.objects.all().order_by('-id').first()
                if last_invoice and last_invoice.invoice_number:
                    try:
                        invoice_number = int(last_invoice.invoice_number.split('-')[-1])
                        next_invoice_number = invoice_number + 1
                    except (ValueError, IndexError):
                        next_invoice_number = 1
                else:
                    next_invoice_number = 1
                
                invoice = Invoice.objects.create(
                    booking=booking,
                    invoice_number=f"INV-{next_invoice_number:04d}",
                    subtotal=subtotal,
                    discount_amount=discount_amount,
                    tax=tax_amount,
                    total=total,
                    due_date=booking.check_out + timedelta(days=1)
                )
                op.success(f"Invoice {invoice.invoice_number} created for booking {booking.confirmation_code}")
                
                # Automatically create payment for the invoice
                from apps.hostel.models import Payment
                from utils.enums import PaymentMethod, PaymentStatus
                import random
                import string
                
                try:
                    # Generate random transaction_id, receipt_number, and reference
                    transaction_id = f"TXN-{uuid.uuid4().hex[:12].upper()}"
                    receipt_number = f"RCP-{random.randint(100000, 999999)}"
                    reference = f"REF-{''.join(random.choices(string.ascii_uppercase + string.digits, k=8))}"
                    
                    payment = Payment.objects.create(
                        invoice=invoice,
                        amount=total,
                        method=PaymentMethod.CASH.value,
                        payment_status=PaymentStatus.PENDING.value,
                        transaction_id=transaction_id,
                        receipt_number=receipt_number,
                        reference=reference
                    )
                    op.success(f"Payment {payment.transaction_id} created for invoice {invoice.invoice_number}")
                except Exception as payment_error:
                    op.fail(f"Failed to create payment: {str(payment_error)}", exc=payment_error)
            except Exception as invoice_error:
                op.fail(f"Failed to create invoice: {str(invoice_error)}", exc=invoice_error)
            
            AuditLogger.log_create(Booking.__name__, performed_by=user, metadata=serialize_for_audit(validated_data))
            op.success(f"Booking {booking.confirmation_code} created successfully and guest profile updated")
            result_serializer = BookingSerializer(booking)
            return BaseResultWithData(
                data=result_serializer.data,
                status_code=HTTPStatus.CREATED,
                message="Booking created successfully"
            )
        except Exception as e:
            op.fail(f"Failed to create booking: {str(e)}", exc=e)
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.BAD_REQUEST,
                message=str(e)
            )
    
    @staticmethod
    def Update(booking_id, data, user=None):
        op = OperationLogger("BookingCommand.Update", booking_id=booking_id)
        op.start()
        
        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            op.fail(f"Booking with id {booking_id} not found")
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.NOT_FOUND,
                message="Booking not found"
            )
        
        if booking.is_deleted:
            op.fail(f"Booking with id {booking_id} is deleted and cannot be updated")
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.BAD_REQUEST,
                message="This booking is deleted and cannot be updated until it is restored"
            )
        
        # Check if guest is being updated and if it's deleted
        if 'guest' in data:
            try:
                guest = GuestProfile.objects.get(id=data['guest'])
                if guest.is_deleted:
                    op.fail(f"Guest with id {data['guest']} is deleted")
                    return BaseResultWithData(
                        data=None,
                        status_code=HTTPStatus.BAD_REQUEST,
                        message="The selected guest is deleted. Please select another guest or restore the deleted one"
                    )
            except GuestProfile.DoesNotExist:
                op.fail(f"Guest with id {data['guest']} not found")
                return BaseResultWithData(
                    data=None,
                    status_code=HTTPStatus.NOT_FOUND,
                    message="Guest not found"
                )
        
        # Check if room is being updated and if it or its floor is deleted
        if 'room' in data:
            from apps.hostel.models import Room
            from utils.enums import RoomStatus
            try:
                room = Room.objects.get(id=data['room'])
                if room.is_deleted:
                    op.fail(f"Room with id {data['room']} is deleted")
                    return BaseResultWithData(
                        data=None,
                        status_code=HTTPStatus.BAD_REQUEST,
                        message="The selected room is deleted. Please select another room or restore the deleted one"
                    )
                if room.floor and room.floor.is_deleted:
                    op.fail(f"Floor with id {room.floor.id} is deleted")
                    return BaseResultWithData(
                        data=None,
                        status_code=HTTPStatus.BAD_REQUEST,
                        message="The floor of the selected room is deleted. Please select a room from a non-deleted floor or restore the deleted floor"
                    )
                if room.status != RoomStatus.AVAILABLE.value:
                    op.fail(f"Room with id {data['room']} is not available")
                    return BaseResultWithData(
                        data=None,
                        status_code=HTTPStatus.BAD_REQUEST,
                        message=f"The selected room is not available (current status: {room.status}). Please select another available room"
                    )
                # Check if number of guests exceeds room occupancy
                number_of_guests = data.get('number_of_guests', booking.number_of_guests)
                if number_of_guests > room.room_type.max_occupancy:
                    op.fail(f"Number of guests ({number_of_guests}) exceeds room max occupancy ({room.room_type.max_occupancy})")
                    return BaseResultWithData(
                        data=None,
                        status_code=HTTPStatus.BAD_REQUEST,
                        message=f"The number of guests ({number_of_guests}) exceeds the room's maximum occupancy ({room.room_type.max_occupancy}). Please select a larger room or reduce the number of guests"
                    )
            except Room.DoesNotExist:
                op.fail(f"Room with id {data['room']} not found")
                return BaseResultWithData(
                    data=None,
                    status_code=HTTPStatus.NOT_FOUND,
                    message="Room not found"
                )
        else:
            # If room is not being changed, check if number_of_guests is being updated
            if 'number_of_guests' in data:
                room = booking.room
                number_of_guests = data['number_of_guests']
                if number_of_guests > room.room_type.max_occupancy:
                    op.fail(f"Number of guests ({number_of_guests}) exceeds room max occupancy ({room.room_type.max_occupancy})")
                    return BaseResultWithData(
                        data=None,
                        status_code=HTTPStatus.BAD_REQUEST,
                        message=f"The number of guests ({number_of_guests}) exceeds the room's maximum occupancy ({room.room_type.max_occupancy}). Please reduce the number of guests or change the room"
                    )
        
        # Validate check-in and check-out dates if being updated
        from django.utils import timezone
        from django.utils.dateparse import parse_date
        
        check_in = data.get('check_in', booking.check_in)
        check_out = data.get('check_out', booking.check_out)
        
        # Parse check_in if it's a string
        if isinstance(check_in, str):
            check_in = parse_date(check_in)
        
        # Parse check_out if it's a string
        if isinstance(check_out, str):
            check_out = parse_date(check_out)
        
        if 'check_in' in data and data['check_in']:
            check_in_date = parse_date(data['check_in']) if isinstance(data['check_in'], str) else data['check_in']
            if check_in_date and check_in_date < timezone.now().date():
                op.fail("Check-in date must be today or in the future")
                return BaseResultWithData(
                    data=None,
                    status_code=HTTPStatus.BAD_REQUEST,
                    message="Check-in date must be today or in the future"
                )
        
        if check_in and check_out and check_out < check_in:
            op.fail("Check-out date must be same or after check-in date")
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.BAD_REQUEST,
                message="Check-out date must be same or after check-in date"
            )
        
        serializer = BookingSerializer(booking, data=data, partial=True)
        if not serializer.is_valid():
            op.fail(f"Validation failed: {serializer.errors}")
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.BAD_REQUEST,
                message=f"Validation failed: {serializer.errors}"
            )
        
        try:
            old_data = {field: getattr(booking, field) for field in serializer.validated_data.keys()}
            updated_booking = serializer.save()
            AuditLogger.log_update(Booking.__name__, performed_by=user, old_values=serialize_for_audit(old_data), new_values=serialize_for_audit(serializer.validated_data))
            op.success(f"Booking {updated_booking.confirmation_code} updated successfully")
            result_serializer = BookingSerializer(updated_booking)
            return BaseResultWithData(
                data=result_serializer.data,
                status_code=HTTPStatus.OK,
                message="Booking updated successfully"
            )
        except Exception as e:
            op.fail(f"Failed to update booking: {str(e)}", exc=e)
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.BAD_REQUEST,
                message=str(e)
            )
    
    @staticmethod
    def ToggleDelete(booking_id, user=None):
        op = OperationLogger("BookingCommand.ToggleDelete", booking_id=booking_id)
        op.start()
        
        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            op.fail(f"Booking with id {booking_id} not found")
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.NOT_FOUND,
                message="Booking not found"
            )
        
        try:
            # Toggle the is_deleted flag
            old_is_deleted = booking.is_deleted
            booking.is_deleted = not booking.is_deleted
            booking.save()
            
            action = "restored" if not booking.is_deleted else "deleted"
            AuditLogger.log_update(
                Booking.__name__, 
                performed_by=user, 
                old_values={"is_deleted": old_is_deleted},
                new_values={"is_deleted": booking.is_deleted}
            )
            op.success(f"Booking {booking.confirmation_code} {action} successfully")
            result_serializer = BookingSerializer(booking)
            return BaseResultWithData(
                data=result_serializer.data,
                status_code=HTTPStatus.OK,
                message=f"Booking {action} successfully"
            )
        except Exception as e:
            op.fail(f"Failed to toggle delete booking: {str(e)}", exc=e)
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.BAD_REQUEST,
                message=str(e)
            )
