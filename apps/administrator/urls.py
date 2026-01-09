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
                path("update/", HotelUpdateAPIView.as_view(), name="hotel-update"),
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
]