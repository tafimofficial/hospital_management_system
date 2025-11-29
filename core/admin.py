from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Notification

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_patient', 'is_doctor', 'is_staff', 'is_active')
    list_filter = ('is_patient', 'is_doctor', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('User Type', {'fields': ('is_patient', 'is_doctor')}),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('User Type', {'fields': ('is_patient', 'is_doctor')}),
    )

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'notification_type', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('user__username', 'user__email', 'title', 'message')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Notification Info', {
            'fields': ('user', 'title', 'message', 'notification_type')
        }),
        ('Status', {
            'fields': ('is_read', 'created_at')
        }),
        ('Related Data', {
            'fields': ('related_object_id', 'link'),
            'classes': ('collapse',)
        }),
    )
