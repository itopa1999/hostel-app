from django.contrib import admin
from django.utils.html import format_html
from apps.administrator.models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    """Custom admin for AuditLog with detailed tracking."""
    list_display = ('action_display', 'entity', 'status_display', 'performed_by', 'target_user', 'created_at')
    list_display_links = ('action_display', 'entity')
    search_fields = ('performed_by__username', 'target_user__username', 'description', 'action', 'entity')
    list_filter = ('action', 'status', 'entity', 'created_at')
    readonly_fields = ('created_at', 'modified_at', 'old_values', 'new_values', 'metadata', 'action', 'entity', 'status', 'description', 'performed_by', 'target_user')
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    list_per_page = 50
    
    fieldsets = (
        ('Action Details', {
            'fields': ('action', 'entity', 'status', 'description')
        }),
        ('Users Involved', {
            'fields': ('performed_by', 'target_user')
        }),
        ('Changes', {
            'fields': ('old_values', 'new_values'),
            'classes': ('collapse',)
        }),
        ('Additional Info', {
            'fields': ('metadata',),
            'classes': ('collapse',)
        }),
        ("Base Model Info", {
            "fields": ("created_at", "modified_at", "deleted_at", "created_by", "modified_by", "deleted_by"),
            "classes": ("collapse",)
        }),
    )
    
    def action_display(self, obj):
        """Display action with color coding"""
        color_map = {
            'CREATE': '#28a745',
            'READ': '#17a2b8',
            'UPDATE': '#ffc107',
            'DELETE': '#dc3545',
            'LOGIN': '#007bff',
            'LOGOUT': '#6c757d',
            'CHANGE_PASSWORD': '#fd7e14',
            'TOGGLE_DELETE': '#dc3545',
        }
        color = color_map.get(obj.action, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.action
        )
    action_display.short_description = 'Action'
    
    def status_display(self, obj):
        """Display status with color coding"""
        if obj.status == 'SUCCESS':
            return format_html('<span style="color: green;">●</span> Success')
        elif obj.status == 'FAILED':
            return format_html('<span style="color: red;">●</span> Failed')
        else:
            return format_html('<span style="color: orange;">●</span> Pending')
    status_display.short_description = 'Status'

