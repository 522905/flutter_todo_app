from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'priority', 'is_completed', 'due_date', 'created_at')
    list_filter = ('category', 'priority', 'is_completed', 'created_at')
    search_fields = ('title', 'description', 'user__email')
    readonly_fields = ('id', 'created_at', 'updated_at', 'completed_at', 'deleted_at')
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Task Information', {
            'fields': ('user', 'title', 'description', 'category', 'priority')
        }),
        ('Status', {
            'fields': ('is_completed', 'completed_at')
        }),
        ('Dates & Reminders', {
            'fields': ('due_date', 'reminder_time')
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at', 'deleted_at'),
            'classes': ('collapse',)
        }),
    )
