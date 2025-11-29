from django.db import models
from django.conf import settings

class BloodInventory(models.Model):
    BLOOD_GROUPS = (
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    )
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUPS, unique=True)
    bags_available = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.blood_group}: {self.bags_available} bags"

class BloodDonor(models.Model):
    BLOOD_GROUPS = BloodInventory.BLOOD_GROUPS
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100, default="Anonymous")
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUPS)
    contact_number = models.CharField(max_length=15)
    last_donation_date = models.DateField(null=True, blank=True)
    is_anonymous = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='approved')
    
    def __str__(self):
        return f"{self.name} ({self.blood_group}) - {self.status}"

class BloodRequest(models.Model):
    BLOOD_GROUPS = BloodInventory.BLOOD_GROUPS
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('fulfilled', 'Fulfilled'),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    patient_name = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUPS)
    units_needed = models.PositiveIntegerField(default=1)
    contact_number = models.CharField(max_length=15)
    hospital_name = models.CharField(max_length=200)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    request_date = models.DateTimeField(auto_now_add=True)
    units_approved = models.PositiveIntegerField(default=0)
    admin_comment = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Request: {self.patient_name} - {self.blood_group} ({self.units_needed} units)"
