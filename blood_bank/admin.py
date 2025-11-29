from django.contrib import admin
from .models import BloodInventory, BloodDonor, BloodRequest

@admin.register(BloodInventory)
class BloodInventoryAdmin(admin.ModelAdmin):
    list_display = ('blood_group', 'bags_available', 'last_updated')
    list_filter = ('blood_group', 'last_updated')
    search_fields = ('blood_group',)
    ordering = ('blood_group',)
    readonly_fields = ('last_updated',)
    
    fieldsets = (
        ('Blood Group', {
            'fields': ('blood_group',)
        }),
        ('Inventory', {
            'fields': ('bags_available', 'last_updated')
        }),
    )

@admin.register(BloodDonor)
class BloodDonorAdmin(admin.ModelAdmin):
    list_display = ('name', 'blood_group', 'contact_number', 'status', 'last_donation_date')
    list_filter = ('blood_group', 'status', 'last_donation_date')
    search_fields = ('name', 'contact_number')
    ordering = ('-last_donation_date',)
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('user', 'name', 'contact_number')
        }),
        ('Donation Details', {
            'fields': ('blood_group', 'last_donation_date', 'status', 'is_anonymous')
        }),
    )
    
    actions = ['approve_donors', 'reject_donors']
    
    def approve_donors(self, request, queryset):
        updated = queryset.update(status='approved')
        self.message_user(request, f'{updated} donor(s) approved successfully.')
    approve_donors.short_description = "Approve selected donors"
    
    def reject_donors(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f'{updated} donor(s) rejected.')
    reject_donors.short_description = "Reject selected donors"

@admin.register(BloodRequest)
class BloodRequestAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'blood_group', 'units_needed', 'units_approved', 'status', 'request_date', 'user')
    list_filter = ('blood_group', 'status', 'request_date')
    search_fields = ('patient_name', 'contact_number', 'user__username', 'user__email')
    ordering = ('-request_date',)
    date_hierarchy = 'request_date'
    
    fieldsets = (
        ('Patient Information', {
            'fields': ('user', 'patient_name', 'contact_number', 'hospital_name')
        }),
        ('Blood Request Details', {
            'fields': ('blood_group', 'units_needed', 'reason')
        }),
        ('Admin Response', {
            'fields': ('status', 'units_approved', 'admin_comment')
        }),
        ('Metadata', {
            'fields': ('request_date',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('request_date',)
    
    actions = ['approve_requests', 'reject_requests']
    
    def approve_requests(self, request, queryset):
        updated = queryset.update(status='approved')
        self.message_user(request, f'{updated} blood request(s) approved successfully.')
    approve_requests.short_description = "Approve selected blood requests"
    
    def reject_requests(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f'{updated} blood request(s) rejected.')
    reject_requests.short_description = "Reject selected blood requests"
