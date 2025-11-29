from django import forms
from .models import DoctorProfile

class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = DoctorProfile
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=False)

    class Meta:
        model = DoctorProfile
        fields = ['specialization', 'address', 'phone_number', 'profile_pic']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        profile = super().save(commit=False)
        if self.cleaned_data.get('first_name'):
            profile.user.first_name = self.cleaned_data['first_name']
        if self.cleaned_data.get('last_name'):
            profile.user.last_name = self.cleaned_data['last_name']
        if self.cleaned_data.get('email'):
            profile.user.email = self.cleaned_data['email']
        if commit:
            profile.user.save()
            profile.save()
        return profile
