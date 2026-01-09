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
                path("update/<int:user_id>/", UpdateUserViewAPI.as_view()),
                path("delete/<int:user_id>/", ToggleDeleteUserViewAPI.as_view()),
            ]
        )
    ),
    path(
        "hotel/",
        include(
            [
                path("update/<int:hotel_id>/", HotelUpdateAPIView.as_view(), name="hotel-update"),
                path("dashboard/", DashboardAPIView.as_view(), name="dashboard"),
            ]
        )
    )
    
]