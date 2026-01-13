from http import HTTPStatus
from apps.hostel.models import GuestProfile
from apps.hostel.serializers import GuestProfileSerializer
from utils.base_result import BaseResultWithData


class GuestProfileQuery:
    
    @staticmethod
    def GetAll():
        try:
            guests = GuestProfile.objects.all()
            serializer = GuestProfileSerializer(guests, many=True)
            return BaseResultWithData(
                data=serializer.data,
                status_code=HTTPStatus.OK,
                message="Guest profiles retrieved successfully"
            )
        except Exception as e:
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.BAD_REQUEST,
                message=str(e)
            )
    
    @staticmethod
    def GetById(guest_id):
        try:
            guest = GuestProfile.objects.get(id=guest_id)
            serializer = GuestProfileSerializer(guest)
            return BaseResultWithData(
                data=serializer.data,
                status_code=HTTPStatus.OK,
                message="Guest profile retrieved successfully"
            )
        except GuestProfile.DoesNotExist:
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.NOT_FOUND,
                message="Guest profile not found"
            )
        except Exception as e:
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.BAD_REQUEST,
                message=str(e)
            )
