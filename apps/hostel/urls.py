from django.urls import path, include
from apps.hostel.views import *

urlpatterns = [
    # Hotel Management
    path(
        "hotel/",
        include(
            [
                
            ]
        )
    )
    
]