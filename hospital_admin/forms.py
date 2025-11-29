from django import forms
from .models import Service

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'category', 'description', 'icon', 'contact_number', 'is_active', 'order']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'icon': forms.TextInput(attrs={'placeholder': 'e.g., fa-ambulance, fa-stethoscope'}),
            'contact_number': forms.TextInput(attrs={'placeholder': 'e.g., +880-XXX-XXXXXX'}),
        }
