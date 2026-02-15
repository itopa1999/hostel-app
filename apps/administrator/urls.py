from django.urls import path, include
from apps.administrator.views import *

urlpatterns = [
    # Admin Hostel Management
    path(
        "admin/",
        include(
            [
                path("create/", UserCreateViewAPI.as_view()),
                path("change-password/", ChangeUserPasswordViewAPI.as_view()),
                path("delete/<int:user_id>/", ToggleDeleteUserViewAPI.as_view()),
            ]
        )
    ),
    path(
        "hotel/",
        include(
            [
                path("update/", HotelUpdateAPIView.as_view(), name="hotel-update"),
                path("details/", HotelDetailAPIView.as_view(), name="hotel-detail"),
                path("dashboard/", DashboardAPIView.as_view(), name="dashboard"),
            ]
        )
    ),
    # Floor endpoints
    path(
        "floor/",
        include(
            [
                path("create/", FloorCreateAPIView.as_view(), name='floor-create'),
                path("list/", FloorListAPIView.as_view(), name='floor-list'),
                path("<int:floor_id>/", FloorDetailAPIView.as_view(), name='floor-detail'),
                path("<int:floor_id>/update/", FloorUpdateAPIView.as_view(), name='floor-update'),
                path("<int:floor_id>/delete/", FloorDeleteAPIView.as_view(), name='floor-delete'),
            ]
        )
    ),
    # Room Type endpoints
    path(
        "room-type/",
        include(
            [
                path("create/", RoomTypeCreateAPIView.as_view(), name='room-type-create'),
                path("list/", RoomTypeListAPIView.as_view(), name='room-type-list'),
                path("<int:room_type_id>/", RoomTypeDetailAPIView.as_view(), name='room-type-detail'),
                path("<int:room_type_id>/update/", RoomTypeUpdateAPIView.as_view(), name='room-type-update'),
                path("<int:room_type_id>/delete/", RoomTypeDeleteAPIView.as_view(), name='room-type-delete'),
            ]
        )
    ),
    # Room endpoints
    path(
        "room/",
        include(
            [
                path("create/", RoomCreateAPIView.as_view(), name='room-create'),
                path("list/", RoomListAPIView.as_view(), name='room-list'),
                path("<int:room_id>/", RoomDetailAPIView.as_view(), name='room-detail'),
                path("<int:room_id>/update/", RoomUpdateAPIView.as_view(), name='room-update'),
                path("<int:room_id>/delete/", RoomDeleteAPIView.as_view(), name='room-delete'),
            ]
        )
    ),
    # Guest Profile endpoints
    path(
        "guest/",
        include(
            [
                path("create/", GuestProfileCreateAPIView.as_view(), name='guest-create'),
                path("list/", GuestProfileListAPIView.as_view(), name='guest-list'),
                path("<int:guest_id>/", GuestProfileDetailAPIView.as_view(), name='guest-detail'),
                path("<int:guest_id>/update/", GuestProfileUpdateAPIView.as_view(), name='guest-update'),
                path("<int:guest_id>/delete/", GuestProfileDeleteAPIView.as_view(), name='guest-delete'),
            ]
        )
    ),
    # Booking endpoints
    path(
        "booking/",
        include(
            [
                path("create/", BookingCreateAPIView.as_view(), name='booking-create'),
                path("list/", BookingListAPIView.as_view(), name='booking-list'),
                path("<int:booking_id>/", BookingDetailAPIView.as_view(), name='booking-detail'),
                path("<int:booking_id>/update/", BookingUpdateAPIView.as_view(), name='booking-update'),
                path("<int:booking_id>/delete/", BookingToggleDeleteAPIView.as_view(), name='booking-delete'),
                path("<int:booking_id>/check-in/", BookingCheckInAPIView.as_view(), name='booking-check-in'),
            ]
        )
    ),
    # Invoice endpoints
    path(
        "invoice/",
        include(
            [
                path("create/", InvoiceCreateAPIView.as_view(), name='invoice-create'),
                path("list/", InvoiceListAPIView.as_view(), name='invoice-list'),
                path("<int:invoice_id>/", InvoiceDetailAPIView.as_view(), name='invoice-detail'),
            ]
        )
    ),
    # Payment endpoints
    path(
        "payment/",
        include(
            [
                path("list/", PaymentListAPIView.as_view(), name='payment-list'),
                path("<int:payment_id>/", PaymentDetailAPIView.as_view(), name='payment-detail'),
                path("<int:payment_id>/update-status/", PaymentUpdateStatusAPIView.as_view(), name='payment-update-status'),
                path("<int:payment_id>/delete/", PaymentToggleDeleteAPIView.as_view(), name='payment-delete'),
            ]
        )
    ),
    # Report endpoints
    path(
        "reports/",
        include(
            [
                path("occupancy/", OccupancyReportAPIView.as_view(), name='occupancy-report'),
                path("revenue/", RevenueReportAPIView.as_view(), name='revenue-report'),
                path("sales/", SalesReportAPIView.as_view(), name='sales-report'),
                path("export/", ExportReportAPIView.as_view(), name='export-report'),
            ]
        )
    ),
    # Settings endpoints
    path(
        "settings/",
        include(
            [
                path("general/", SettingsAPIView.as_view(), name='general-settings'),
            ]
        )
    ),
]