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
                path("detail/", UserDetailViewAPI.as_view()),
                path("update/", UpdateUserViewAPI.as_view()),
                path("groups/", GroupListAPIView.as_view(), name="group-list"),
                path("list/", UserListAPIView.as_view(), name="user-list"),
                path("create/", UserCreateAPIView.as_view(), name="user-create"),
                path("<int:user_id>/delete/", UserDeleteAPIView.as_view(), name="user-delete"),
                path("<int:user_id>/update-groups/", UserUpdateGroupsAPIView.as_view(), name="user-update-groups"),
            ]
        )
    )
]
