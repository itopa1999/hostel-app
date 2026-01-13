from http import HTTPStatus
from apps.hostel.models import Invoice
from apps.hostel.serializers import InvoiceSerializer
from utils.base_result import BaseResultWithData


class InvoiceQuery:
    
    @staticmethod
    def GetAll():
        try:
            invoices = Invoice.objects.all()
            serializer = InvoiceSerializer(invoices, many=True)
            return BaseResultWithData(
                data=serializer.data,
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
            invoice = Invoice.objects.get(id=invoice_id)
            serializer = InvoiceSerializer(invoice)
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
