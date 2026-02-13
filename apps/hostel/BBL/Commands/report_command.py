from http import HTTPStatus
from datetime import datetime, timedelta
from django.db.models import Count, Sum, Q, F
from apps.hostel.models import Booking, Invoice, Payment, Room, RoomType
from utils.base_result import BaseResultWithData
from utils.log_helpers import OperationLogger
from utils.enums import BookingStatus, PaymentStatus, RoomStatus
from decimal import Decimal


class ReportCommand:
    
    @staticmethod
    def GenerateOccupancyReport(date_str=None):
        """Generate occupancy report for a specific date"""
        op = OperationLogger("ReportCommand.GenerateOccupancyReport", date=date_str)
        op.start()
        
        try:
            # Parse date
            if date_str:
                target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            else:
                target_date = datetime.now().date()
            
            # Get total rooms
            total_rooms = Room.objects.filter(is_deleted=False).count()
            
            # Get occupied rooms on the specific date (only CHECKED_IN, not CHECKED_OUT)
            occupied_rooms = Booking.objects.filter(
                is_deleted=False,
                check_in__lte=target_date,
                check_out__gt=target_date,
                status=BookingStatus.CHECKED_IN.value
            ).count()
            
            # Get available rooms
            available_rooms = total_rooms - occupied_rooms
            
            # Calculate occupancy rate
            occupancy_rate = (occupied_rooms / total_rooms * 100) if total_rooms > 0 else 0
            
            # Get rooms by type for detailed breakdown
            room_types_breakdown = RoomType.objects.annotate(
                total_rooms=Count('rooms'),
                occupied_count=Count('rooms__bookings', filter=Q(
                    rooms__bookings__is_deleted=False,
                    rooms__bookings__check_in__lte=target_date,
                    rooms__bookings__check_out__gt=target_date,
                    rooms__bookings__status=BookingStatus.CHECKED_IN.value
                ))
            ).values('name', 'total_rooms', 'occupied_count')
            
            room_types_data = []
            for rt in room_types_breakdown:
                room_types_data.append({
                    'room_type': rt['name'],
                    'total': rt['total_rooms'],
                    'occupied': rt['occupied_count'],
                    'available': rt['total_rooms'] - rt['occupied_count'],
                    'occupancy_rate': (rt['occupied_count'] / rt['total_rooms'] * 100) if rt['total_rooms'] > 0 else 0
                })
            
            report_data = {
                'report_date': target_date.strftime('%Y-%m-%d'),
                'total_rooms': total_rooms,
                'occupied_rooms': occupied_rooms,
                'available_rooms': available_rooms,
                'occupancy_rate': round(occupancy_rate, 2),
                'room_types_breakdown': room_types_data
            }
            
            op.success(f"Occupancy report generated for {target_date}")
            return BaseResultWithData(
                data=report_data,
                status_code=HTTPStatus.OK,
                message="Occupancy report generated successfully"
            )
        except Exception as e:
            op.fail(f"Failed to generate occupancy report: {str(e)}", exc=e)
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.BAD_REQUEST,
                message=str(e)
            )
    
    @staticmethod
    def GenerateRevenueReport(date_str=None):
        """Generate revenue report for a specific date or date range"""
        op = OperationLogger("ReportCommand.GenerateRevenueReport", date=date_str)
        op.start()
        
        try:
            # Parse date
            if date_str:
                target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            else:
                target_date = datetime.now().date()
            
            # Get invoices with payment date on the specific date
            completed_invoices = Invoice.objects.filter(
                is_deleted=False,
                payment_date=target_date,
                payment_status=PaymentStatus.COMPLETED.value
            )
            
            # Calculate total revenue
            total_revenue = completed_invoices.aggregate(total=Sum('total'))['total'] or Decimal('0.00')
            
            # Calculate breakdown by room type
            revenue_by_room_type = completed_invoices.values('booking__room__room_type__name').annotate(
                total=Sum('total'),
                count=Count('id')
            )
            
            room_type_breakdown = []
            for item in revenue_by_room_type:
                room_type_breakdown.append({
                    'room_type': item['booking__room__room_type__name'],
                    'total_revenue': float(item['total']),
                    'number_of_bookings': item['count']
                })
            
            # Calculate discount and tax summary
            total_discount = completed_invoices.aggregate(discount=Sum('discount_amount'))['discount'] or Decimal('0.00')
            total_tax = completed_invoices.aggregate(tax=Sum('tax'))['tax'] or Decimal('0.00')
            total_subtotal = completed_invoices.aggregate(subtotal=Sum('subtotal'))['subtotal'] or Decimal('0.00')
            
            report_data = {
                'report_date': target_date.strftime('%Y-%m-%d'),
                'total_completed_bookings': completed_invoices.count(),
                'total_subtotal': float(total_subtotal),
                'total_discount': float(total_discount),
                'total_tax': float(total_tax),
                'total_revenue': float(total_revenue),
                'room_type_breakdown': room_type_breakdown
            }
            
            op.success(f"Revenue report generated for {target_date}")
            return BaseResultWithData(
                data=report_data,
                status_code=HTTPStatus.OK,
                message="Revenue report generated successfully"
            )
        except Exception as e:
            op.fail(f"Failed to generate revenue report: {str(e)}", exc=e)
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.BAD_REQUEST,
                message=str(e)
            )
    
    @staticmethod
    def GenerateSalesReport(date_str=None):
        """Generate sales report for a specific date"""
        op = OperationLogger("ReportCommand.GenerateSalesReport", date=date_str)
        op.start()
        
        try:
            # Parse date
            if date_str:
                target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            else:
                target_date = datetime.now().date()
            
            # Get bookings created on the specific date
            bookings_created = Booking.objects.filter(
                is_deleted=False,
                created_at__date=target_date
            )
            
            # Get payments made on the specific date
            payments_completed = Payment.objects.filter(
                is_deleted=False,
                created_at__date=target_date,
                payment_status=PaymentStatus.COMPLETED.value
            )
            
            # Calculate total sales
            total_sales = payments_completed.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
            
            # Breakdown by payment method
            sales_by_method = payments_completed.values('method').annotate(
                total=Sum('amount'),
                count=Count('id')
            )
            
            payment_method_breakdown = []
            for item in sales_by_method:
                payment_method_breakdown.append({
                    'payment_method': item['method'],
                    'total_amount': float(item['total']),
                    'number_of_transactions': item['count']
                })
            
            # New bookings by status
            bookings_by_status = bookings_created.values('status').annotate(count=Count('id'))
            
            status_breakdown = []
            for item in bookings_by_status:
                status_breakdown.append({
                    'status': item['status'],
                    'count': item['count']
                })
            
            report_data = {
                'report_date': target_date.strftime('%Y-%m-%d'),
                'new_bookings': bookings_created.count(),
                'completed_payments': payments_completed.count(),
                'total_sales': float(total_sales),
                'payment_method_breakdown': payment_method_breakdown,
                'new_bookings_by_status': status_breakdown
            }
            
            op.success(f"Sales report generated for {target_date}")
            return BaseResultWithData(
                data=report_data,
                status_code=HTTPStatus.OK,
                message="Sales report generated successfully"
            )
        except Exception as e:
            op.fail(f"Failed to generate sales report: {str(e)}", exc=e)
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.BAD_REQUEST,
                message=str(e)
            )
    
    @staticmethod
    def GenerateExportReport(date_str=None):
        """Generate export/summary report for a specific date"""
        op = OperationLogger("ReportCommand.GenerateExportReport", date=date_str)
        op.start()
        
        try:
            # Parse date
            if date_str:
                target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            else:
                target_date = datetime.now().date()
            
            # Combine data from other reports for comprehensive export
            occupancy_result = ReportCommand.GenerateOccupancyReport(date_str)
            revenue_result = ReportCommand.GenerateRevenueReport(date_str)
            sales_result = ReportCommand.GenerateSalesReport(date_str)
            
            if not all([occupancy_result.data, revenue_result.data, sales_result.data]):
                return BaseResultWithData(
                    data=None,
                    status_code=HTTPStatus.BAD_REQUEST,
                    message="Failed to generate export report"
                )
            
            report_data = {
                'report_date': target_date.strftime('%Y-%m-%d'),
                'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'occupancy_report': occupancy_result.data,
                'revenue_report': revenue_result.data,
                'sales_report': sales_result.data
            }
            
            op.success(f"Export report generated for {target_date}")
            return BaseResultWithData(
                data=report_data,
                status_code=HTTPStatus.OK,
                message="Export report generated successfully"
            )
        except Exception as e:
            op.fail(f"Failed to generate export report: {str(e)}", exc=e)
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.BAD_REQUEST,
                message=str(e)
            )
