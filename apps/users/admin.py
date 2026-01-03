from django.contrib import admin
from django.utils.html import format_html
from apps.users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Custom admin for User with admin.ModelAdmin integration."""
    list_display = (
       "username" ,"email", "full_name_display", "id_number", "status_display", "created_at"
    )
    list_display_links = ("username" ,"email", "full_name_display")
    search_fields = ("username" ,"email", "first_name", "last_name", "id_number",)
    list_filter = ("is_active", "is_staff", "is_superuser", "created_at", "groups")
    readonly_fields = ("date_joined", "last_login", "created_at", "modified_at")
    filter_horizontal = ("groups", "user_permissions")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    list_per_page = 50

    fieldsets = (
        ("Personal Information", {
            "fields": (
                "username",
                "email",
                "first_name",
                "last_name",
                "id_number",
            ),
        }),
        ("Permissions & Access", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            ),
        }),
        ("Password", {
            "fields": ("password",),
        }),
        ("Important Dates", {
            "fields": ("date_joined", "last_login"),
        }),
        ("Base Model Info", {
            "fields": ("created_at", "modified_at", "created_by", "modified_by", "is_deleted", "deleted_at", "deleted_by"),
            "classes": ("collapse",)
        }),
    )

    def full_name_display(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name_display.short_description = "Full Name"

    def status_display(self, obj):
        if obj.is_active:
            return format_html('<span style="color: green;">●</span> Active')
        return format_html('<span style="color: red;">●</span> Inactive')
    status_display.short_description = "Status"
 