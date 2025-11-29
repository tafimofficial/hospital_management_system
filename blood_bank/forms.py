from django import forms
from .models import BloodDonor, BloodRequest

class BloodDonorForm(forms.ModelForm):
    class Meta:
        model = BloodDonor
        fields = ['name', 'blood_group', 'contact_number', 'last_donation_date', 'is_anonymous']
        widgets = {
            'last_donation_date': forms.DateInput(attrs={'type': 'date'}),
        }

class BloodRequestForm(forms.ModelForm):
    class Meta:
        model = BloodRequest
        fields = ['patient_name', 'blood_group', 'units_needed', 'contact_number', 'hospital_name', 'reason']
