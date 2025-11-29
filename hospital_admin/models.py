from django.db import models

class Service(models.Model):
    CATEGORY_CHOICES = [
        ('emergency', 'Emergency Services'),
        ('consultation', 'Consultation'),
        ('diagnostics', 'Diagnostics & Imaging'),
        ('laboratory', 'Laboratory'),
        ('specialized', 'Specialized Care'),
        ('other', 'Other Services'),
    ]
    
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    description = models.TextField()
    icon = models.CharField(max_length=50, default='fa-hospital', help_text='FontAwesome icon class (e.g., fa-ambulance)')
    contact_number = models.CharField(max_length=20, blank=True, help_text='Contact number for the service (optional)')
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0, help_text='Display order (lower numbers appear first)')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
