from django.urls import path, include
from apps.hostel.views import *

urlpatterns = [
    # Admin Hostel Management
    path(
        "hostel/",
        include(
            [
                # path("", LoginViewAPI.as_view()),
             
            ]
        )
    ),
]