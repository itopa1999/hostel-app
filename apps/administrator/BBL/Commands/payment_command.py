from http import HTTPStatus
from apps.hostel.models import Payment, Invoice, Booking, Room
from apps.hostel.serializers import PaymentSerializer
from utils.base_result import BaseResultWithData
from utils.log_helpers import OperationLogger
from utils.audit.audit_logger import AuditLogger
from utils.serialization_helpers import serialize_for_audit
from utils.enums import PaymentStatus, RoomStatus
from datetime import date


class PaymentCommand:
    
    @staticmethod
    def Update(payment_id, data, user=None):
        op = OperationLogger("PaymentCommand.Update", payment_id=payment_id)
        op.start()
        
        try:
            payment = Payment.objects.get(id=payment_id)
        except Payment.DoesNotExist:
            op.fail(f"Payment with id {payment_id} not found")
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.NOT_FOUND,
                message="Payment not found"
            )
        
        if payment.is_deleted:
            op.fail(f"Payment {payment.transaction_id} is deleted")
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.BAD_REQUEST,
                message="Cannot update a deleted payment"
            )
        
        try:
            # Get the new payment status
            new_status = data.get('payment_status')
            
            if not new_status:
                op.fail("Payment status is required")
                return BaseResultWithData(
                    data=None,
                    status_code=HTTPStatus.BAD_REQUEST,
                    message="Payment status is required"
                )
            
            # Prevent downgrade from COMPLETED status
            if payment.payment_status == PaymentStatus.COMPLETED.value and new_status != PaymentStatus.COMPLETED.value:
                op.fail(f"Payment {payment.transaction_id} is already completed and cannot be changed")
                return BaseResultWithData(
                    data=None,
                    status_code=HTTPStatus.BAD_REQUEST,
                    message="Payment status cannot be changed once marked as completed"
                )
            
            # If payment is being marked as completed, check room status
            if new_status == PaymentStatus.COMPLETED.value:
                # Get related invoice and booking
                invoice = payment.invoice
                booking = invoice.booking
                room = booking.room
                
                # Check if room status is AVAILABLE
                if room.status != RoomStatus.AVAILABLE.value:
                    op.fail(f"Room {room.number} status is {room.status}, not AVAILABLE")
                    return BaseResultWithData(
                        data=None,
                        status_code=HTTPStatus.BAD_REQUEST,
                        message=f"Cannot mark payment as completed. Room {room.number} is currently {room.status}. Please go to the booking section and change the room to an available one before completing payment."
                    )
            
            # Update payment status
            payment.payment_status = new_status
            payment.save()
            op.success(f"Payment {payment.transaction_id} status updated to {new_status}")
            
            # If payment is completed, update related entities
            if new_status == PaymentStatus.COMPLETED.value:
                try:
                    # Get related invoice and booking
                    invoice = payment.invoice
                    booking = invoice.booking
                    room = booking.room
                    
                    # Update invoice payment status and payment_date
                    invoice.payment_status = PaymentStatus.COMPLETED.value
                    invoice.payment_date = date.today()
                    invoice.save()
                    op.success(f"Invoice {invoice.invoice_number} status updated to COMPLETED with payment date {invoice.payment_date}")
                    
                    # Update booking payment status and add payment_date if the field exists
                    booking.payment_status = PaymentStatus.COMPLETED.value
                    booking.save()
                    op.success(f"Booking {booking.confirmation_code} payment status updated to COMPLETED")
                    
                    # Update room status to OCCUPIED
                    room.status = RoomStatus.OCCUPIED.value
                    room.save()
                    op.success(f"Room {room.number} status updated to OCCUPIED")
                    
                except Exception as cascade_error:
                    op.fail(f"Warning: Failed to update related entities: {str(cascade_error)}")
            
            AuditLogger.log_update(Payment.__name__, performed_by=user, metadata=serialize_for_audit({'payment_id': payment.id, 'transaction_id': payment.transaction_id, 'new_status': new_status}))
            op.success(f"Payment {payment.transaction_id} updated successfully")
            
            result_serializer = PaymentSerializer(payment)
            return BaseResultWithData(
                data=result_serializer.data,
                status_code=HTTPStatus.OK,
                message="Payment status updated successfully"
            )
        except Exception as e:
            op.fail(f"Failed to update payment: {str(e)}", exc=e)
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.BAD_REQUEST,
                message=str(e)
            )
