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
            except Room.DoesNotExist:
                op.fail(f"Room with id {data['room']} not found")
                return BaseResultWithData(
                    data=None,
                    status_code=HTTPStatus.NOT_FOUND,
                    message="Room not found"
                )
        
        # Generate confirmation code if not provided
        if 'confirmation_code' not in data or not data.get('confirmation_code'):
            data['confirmation_code'] = f"BK{uuid.uuid4().hex[:10].upper()}"
        
        serializer = BookingSerializer(data=data)
        if not serializer.is_valid():
            op.fail(f"Validation failed: {serializer.errors}")
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.BAD_REQUEST,
                message=f"Validation failed: {serializer.errors}"
            )
        
        try:
            booking = Booking.objects.create(**serializer.validated_data)
            
            # Update GuestProfile - set first_visit_date and increment total_stays
            guest = booking.guest
            if not guest.first_visit_date:
                guest.first_visit_date = booking.check_in
            guest.total_stays += 1
            guest.save()
            
            AuditLogger.log_create(Booking.__name__, performed_by=user, metadata=serialize_for_audit(serializer.validated_data))
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
            except Room.DoesNotExist:
                op.fail(f"Room with id {data['room']} not found")
                return BaseResultWithData(
                    data=None,
                    status_code=HTTPStatus.NOT_FOUND,
                    message="Room not found"
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
