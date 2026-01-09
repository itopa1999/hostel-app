from django.urls import path, include
from apps.hostel.views import *

urlpatterns = [
    # Hotel Management
    path(
        "hotel/",
        include(
            [
                path("create/", HotelCreateAPIView.as_view(), name="hotel-create"),
                path("update/<int:hotel_id>/", HotelUpdateAPIView.as_view(), name="hotel-update"),
                path("dashboard/", DashboardAPIView.as_view(), name="dashboard"),
            ]
        )
    )
    
]