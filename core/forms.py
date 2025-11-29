from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from patient.models import PatientProfile
from doctor.models import DoctorProfile

class PatientRegistrationForm(UserCreationForm):
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
    phone_number = forms.CharField(max_length=15)
    profile_pic = forms.ImageField(required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_patient = True
        if commit:
            user.save()
            PatientProfile.objects.create(
                user=user,
                address=self.cleaned_data['address'],
                phone_number=self.cleaned_data['phone_number'],
                profile_pic=self.cleaned_data['profile_pic']
            )
        return user

class DoctorRegistrationForm(UserCreationForm):
    specialization = forms.CharField(max_length=100)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
    phone_number = forms.CharField(max_length=15)
    profile_pic = forms.ImageField(required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_doctor = True
        if commit:
            user.save()
            DoctorProfile.objects.create(
                user=user,
                specialization=self.cleaned_data['specialization'],
                address=self.cleaned_data['address'],
                phone_number=self.cleaned_data['phone_number'],
                profile_pic=self.cleaned_data['profile_pic'],
                status='pending'
            )
        return user
