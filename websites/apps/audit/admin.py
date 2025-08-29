from django.contrib import admin
from .models import AuditLog

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('action', 'user', 'ip_address', 'path', 'timestamp')
    list_filter = ('action', 'timestamp', 'user')
    search_fields = ('user__username', 'ip_address', 'path')
    readonly_fields = ('user', 'action', 'ip_address', 'path', 'user_agent', 'timestamp', 'additional_data')

    # Disable adding new audit logs through admin.
    def has_add_permission(self, request):
        return False

    # Disable editing existing audit logs.
    def has_change_permission(self, request, obj=None):
        return False

    # Disable deleting audit logs.
    def has_delete_permission(self, request, obj=None):
        return False
