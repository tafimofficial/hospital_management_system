from django.contrib import admin
from .models import DoctorProfile, Appointment

@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'phone_number', 'status')
    list_filter = ('status', 'specialization')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'specialization', 'phone_number')
    ordering = ('-user__date_joined',)
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'status')
        }),
        ('Professional Details', {
            'fields': ('profile_pic', 'specialization')
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'address')
        }),
    )
    
    actions = ['approve_doctors', 'reject_doctors']
    
    def approve_doctors(self, request, queryset):
        updated = queryset.update(status='active')
        self.message_user(request, f'{updated} doctor(s) approved successfully.')
    approve_doctors.short_description = "Approve selected doctors"
    
    def reject_doctors(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f'{updated} doctor(s) rejected.')
    reject_doctors.short_description = "Reject selected doctors"

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'date', 'time', 'status', 'created_at')
    list_filter = ('status', 'date', 'created_at')
    search_fields = ('patient__username', 'patient__email', 'doctor__user__username', 'description')
    ordering = ('-created_at',)
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Appointment Details', {
            'fields': ('patient', 'doctor', 'date', 'time', 'status')
        }),
        ('Description', {
            'fields': ('description',)
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at',)
    
    actions = ['approve_appointments', 'decline_appointments']
    
    def approve_appointments(self, request, queryset):
        updated = queryset.update(status='approved')
        self.message_user(request, f'{updated} appointment(s) approved successfully.')
    approve_appointments.short_description = "Approve selected appointments"
    
    def decline_appointments(self, request, queryset):
        updated = queryset.update(status='declined')
        self.message_user(request, f'{updated} appointment(s) declined.')
    decline_appointments.short_description = "Decline selected appointments"
