from http import HTTPStatus
from datetime import date
from apps.hostel.models import Invoice
from apps.hostel.serializers import InvoiceSerializer
from utils.base_result import BaseResultWithData
from utils.cache_helper import GlobalCache
from utils.enums import CacheKeys


class InvoiceQuery:
    
    @staticmethod
    def GetAll():
        try:
            # Try cache first
            cached_data = GlobalCache.get(CacheKeys.INVOICE_ALL.value)
            if cached_data:
                return BaseResultWithData(
                    data=cached_data,
                    status_code=HTTPStatus.OK,
                    message="Invoices retrieved successfully (cached)"
                )
            
            invoices = Invoice.objects.all()
            serializer = InvoiceSerializer(invoices, many=True)
            
            # Add today's date to each invoice item
            today = date.today().isoformat()
            data_with_date = []
            for item in serializer.data:
                item['today'] = today
                data_with_date.append(item)
            
            # Cache the result
            GlobalCache.set(CacheKeys.INVOICE_ALL.value, data_with_date)
            
            return BaseResultWithData(
                data=data_with_date,
                status_code=HTTPStatus.OK,
                message="Invoices retrieved successfully"
            )
        except Exception as e:
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.BAD_REQUEST,
                message=str(e)
            )
    
    @staticmethod
    def GetById(invoice_id):
        try:
            # Try cache first
            cache_key = CacheKeys.format(CacheKeys.INVOICE_ID, invoice_id=invoice_id)
            cached_data = GlobalCache.get(cache_key)
            if cached_data:
                return BaseResultWithData(
                    data=cached_data,
                    status_code=HTTPStatus.OK,
                    message="Invoice retrieved successfully (cached)"
                )
            
            invoice = Invoice.objects.get(id=invoice_id)
            serializer = InvoiceSerializer(invoice)
            
            # Cache the result
            GlobalCache.set(cache_key, serializer.data)
            
            return BaseResultWithData(
                data=serializer.data,
                status_code=HTTPStatus.OK,
                message="Invoice retrieved successfully"
            )
        except Invoice.DoesNotExist:
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.NOT_FOUND,
                message="Invoice not found"
            )
        except Exception as e:
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.BAD_REQUEST,
                message=str(e)
            )
