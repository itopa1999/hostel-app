from django.urls import path, include
from apps.users.views import *

urlpatterns = [
    # Authentication
    path(
        "user/",
        include(
            [
                path("login/", LoginViewAPI.as_view()),
                path("change-password/", ChangePasswordViewAPI.as_view()),
                path("", UserDetailViewAPI.as_view()),
                path("groups/", GroupListAPIView.as_view(), name="group-list"),
            ]
        )
    )
]
