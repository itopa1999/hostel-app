from http import HTTPStatus
from apps.hostel.models import Invoice, Booking, Payment, Setting
from apps.hostel.serializers import InvoiceSerializer
from utils.base_result import BaseResultWithData
from utils.log_helpers import OperationLogger
from utils.audit.audit_logger import AuditLogger
from utils.serialization_helpers import serialize_for_audit
from utils.enums import PaymentMethod, PaymentStatus
from datetime import timedelta
import uuid
import random
import string


class InvoiceCommand:
    
    @staticmethod
    def Create(data, user=None):
        op = OperationLogger("InvoiceCommand.Create", booking_id=data.get('booking'))
        op.start()
        
        # Check if booking exists
        if 'booking' not in data or not data.get('booking'):
            op.fail("Booking ID is required")
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.BAD_REQUEST,
                message="Booking ID is required"
            )
        
        try:
            booking = Booking.objects.get(id=data['booking'])
        except Booking.DoesNotExist:
            op.fail(f"Booking with id {data['booking']} not found")
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.NOT_FOUND,
                message="Booking not found"
            )
        
        if booking.is_deleted:
            op.fail(f"Booking with id {data['booking']} is deleted")
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.BAD_REQUEST,
                message="The selected booking is deleted. Please select another booking or restore the deleted one"
            )
        
        # Check if invoice already exists for this booking
        if hasattr(booking, 'invoice'):
            op.fail(f"Invoice already exists for booking {booking.confirmation_code}")
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.BAD_REQUEST,
                message="An invoice already exists for this booking"
            )
        
        try:
            # Calculate number of nights for the booking
            nights = (booking.check_out - booking.check_in).days
            if nights == 0:
                nights = 1
            
            # Get effective room price
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
                due_date=booking.check_out + timedelta(days=1),
                notes=data.get('notes', '')
            )
            op.success(f"Invoice {invoice.invoice_number} created for booking {booking.confirmation_code}")
            
            # Automatically create payment for the invoice
            try:
                # Generate random transaction_id, receipt_number, and reference
                transaction_id = f"TXN-{uuid.uuid4().hex[:12].upper()}"
                receipt_number = f"RCP-{random.randint(100000, 999999)}"
                reference = f"REF-{''.join(random.choices(string.ascii_uppercase + string.digits, k=8))}"
                
                payment = Payment.objects.create(
                    invoice=invoice,
                    amount=invoice.total,
                    method=PaymentMethod.CASH.value,
                    payment_status=PaymentStatus.PENDING.value,
                    transaction_id=transaction_id,
                    receipt_number=receipt_number,
                    reference=reference
                )
                op.success(f"Payment {payment.transaction_id} created for invoice {invoice.invoice_number}")
            except Exception as payment_error:
                op.fail(f"Warning: Failed to create payment: {str(payment_error)}")
            
            AuditLogger.log_create(Invoice.__name__, performed_by=user, metadata=serialize_for_audit({'booking_id': booking.id, 'invoice_number': invoice.invoice_number}))
            op.success(f"Invoice {invoice.invoice_number} created successfully with payment")
            result_serializer = InvoiceSerializer(invoice)
            return BaseResultWithData(
                data=result_serializer.data,
                status_code=HTTPStatus.CREATED,
                message="Invoice and payment created successfully"
            )
        except Exception as e:
            op.fail(f"Failed to create invoice: {str(e)}", exc=e)
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.BAD_REQUEST,
                message=str(e)
            )
    
    @staticmethod
    def Update(invoice_id, data, user=None):
        op = OperationLogger("InvoiceCommand.Update", invoice_id=invoice_id)
        op.start()
        
        try:
            invoice = Invoice.objects.get(id=invoice_id)
        except Invoice.DoesNotExist:
            op.fail(f"Invoice with id {invoice_id} not found")
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.NOT_FOUND,
                message="Invoice not found"
            )
        
        if invoice.is_deleted:
            op.fail(f"Invoice {invoice.invoice_number} is deleted")
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.BAD_REQUEST,
                message="Cannot update a deleted invoice"
            )
        
        try:
            # If discount or tax is being updated, recalculate total
            if 'discount_amount' in data or 'tax' in data:
                subtotal = invoice.subtotal
                discount_amount = data.get('discount_amount', invoice.discount_amount)
                tax_amount = data.get('tax', invoice.tax)
                total = subtotal - discount_amount + tax_amount
                
                invoice.discount_amount = discount_amount
                invoice.tax = tax_amount
                invoice.total = total
            
            # Update other fields if provided
            if 'notes' in data:
                invoice.notes = data.get('notes')
            if 'due_date' in data:
                invoice.due_date = data.get('due_date')
            if 'payment_status' in data:
                invoice.payment_status = data.get('payment_status')
            if 'payment_date' in data:
                invoice.payment_date = data.get('payment_date')
            
            invoice.save()
            op.success(f"Invoice {invoice.invoice_number} updated successfully")
            
            AuditLogger.log_update(Invoice.__name__, performed_by=user, metadata=serialize_for_audit({'invoice_id': invoice.id, 'invoice_number': invoice.invoice_number}))
            
            result_serializer = InvoiceSerializer(invoice)
            return BaseResultWithData(
                data=result_serializer.data,
                status_code=HTTPStatus.OK,
                message="Invoice updated successfully"
            )
        except Exception as e:
            op.fail(f"Failed to update invoice: {str(e)}", exc=e)
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.BAD_REQUEST,
                message=str(e)
            )
