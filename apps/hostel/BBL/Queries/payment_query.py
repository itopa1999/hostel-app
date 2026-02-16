from http import HTTPStatus
from apps.hostel.models import Payment
from apps.hostel.serializers import PaymentSerializer
from utils.base_result import BaseResultWithData
from utils.cache_helper import GlobalCache
from utils.enums import CacheKeys


class PaymentQuery:
    
    @staticmethod
    def GetAll():
        try:
            # Try cache first
            cached_data = GlobalCache.get(CacheKeys.PAYMENT_ALL.value)
            if cached_data:
                return BaseResultWithData(
                    data=cached_data,
                    status_code=HTTPStatus.OK,
                    message="Payments retrieved successfully (cached)"
                )
            
            payments = Payment.objects.all()
            serializer = PaymentSerializer(payments, many=True)
            
            # Cache the result
            GlobalCache.set(CacheKeys.PAYMENT_ALL.value, serializer.data)
            
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
            # Try cache first
            cache_key = CacheKeys.format(CacheKeys.PAYMENT_ID, payment_id=payment_id)
            cached_data = GlobalCache.get(cache_key)
            if cached_data:
                return BaseResultWithData(
                    data=cached_data,
                    status_code=HTTPStatus.OK,
                    message="Payment retrieved successfully (cached)"
                )
            
            payment = Payment.objects.get(id=payment_id)
            serializer = PaymentSerializer(payment)
            
            # Cache the result
            GlobalCache.set(cache_key, serializer.data)
            
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
