from django.contrib import admin

from apps.tasks.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['name', 'project', 'status', 'priority', 'deadline', 'created_at']
    list_filter = ['status', 'priority', 'created_at', 'deadline', 'project__user']
    search_fields = ['name', 'project__name', 'project__user__email']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    fieldsets = (
        (None, {'fields': ('name', 'project', 'status', 'priority', 'deadline')}),
        (
            'Timestamps',
            {
                'fields': ('created_at', 'updated_at'),
                'classes': ('collapse',),
            },
        ),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('project', 'project__user')
