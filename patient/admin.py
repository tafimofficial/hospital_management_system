from django.contrib import admin
from .models import PatientProfile

@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'address_preview')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'phone_number')
    ordering = ('-user__date_joined',)
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Contact Details', {
            'fields': ('profile_pic', 'phone_number', 'address')
        }),
    )
    
    def address_preview(self, obj):
        """Show first 50 characters of address"""
        return obj.address[:50] + '...' if len(obj.address) > 50 else obj.address
    address_preview.short_description = 'Address'
    
    def get_readonly_fields(self, request, obj=None):
        # Make user field readonly when editing
        if obj:
            return ('user',)
        return ()
