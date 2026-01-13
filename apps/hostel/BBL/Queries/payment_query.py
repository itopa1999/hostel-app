from http import HTTPStatus
from apps.hostel.models import Payment
from apps.hostel.serializers import PaymentSerializer
from utils.base_result import BaseResultWithData


class PaymentQuery:
    
    @staticmethod
    def GetAll():
        try:
            payments = Payment.objects.all()
            serializer = PaymentSerializer(payments, many=True)
            return BaseResultWithData(
                data=serializer.data,
                status_code=HTTPStatus.OK,
                message="Payments retrieved successfully"
            )
        except Exception as e:
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.BAD_REQUEST,
                message=str(e)
            )
    
    @staticmethod
    def GetById(payment_id):
        try:
            payment = Payment.objects.get(id=payment_id)
            serializer = PaymentSerializer(payment)
            return BaseResultWithData(
                data=serializer.data,
                status_code=HTTPStatus.OK,
                message="Payment retrieved successfully"
            )
        except Payment.DoesNotExist:
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.NOT_FOUND,
                message="Payment not found"
            )
        except Exception as e:
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.BAD_REQUEST,
                message=str(e)
            )
