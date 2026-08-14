from django.contrib import admin
from .models import ActivityLogs


@admin.register(ActivityLogs)
class ActivityLogsAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'action',
        'model_name',
        'object_id',
        'description',
        'timestamp',
    )

    list_filter = (
        'action',
        'model_name',
        'timestamp',
    )

    search_fields = (
        'user__username',
        'user__email',
        'model_name',
        'object_id',
        'description',
    )

    ordering = (
        '-timestamp',
    )

    readonly_fields = (
        'user',
        'action',
        'model_name',
        'object_id',
        'description',
        'timestamp',
    )

    list_per_page = 50

    date_hierarchy = 'timestamp'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False