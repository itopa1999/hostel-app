from django.urls import path, include
from apps.users.views import *

urlpatterns = [
    # Authentication
    path(
        "user/",
        include(
            [
                path("login/", LoginViewAPI.as_view()),
                path("create/", UserCreateViewAPI.as_view()),
                path("change-password/", ChangePasswordViewAPI.as_view()),
            ]
        )
    ),
]
