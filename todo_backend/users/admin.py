from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'created_at')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'email_notifications', 'push_notifications')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('-created_at',)

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Notification Settings', {
            'fields': ('phone_number', 'fcm_token', 'email_notifications',
                      'whatsapp_notifications', 'push_notifications'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
        }),
    )

    readonly_fields = ('created_at', 'updated_at')
