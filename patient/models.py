from django.db import models
from django.conf import settings

class PatientProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='patient_profile')
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    profile_pic = models.ImageField(upload_to='profile_pics/patient/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
