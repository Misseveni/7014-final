# ZHANGXINYUE
# 24077321

from django import forms
from .models import DisasterReport, AidRequest, Shelter, VolunteerProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class DisasterReportForm(forms.ModelForm):
    class Meta:
        model = DisasterReport
        fields = ['disaster_type', 'location', 'gps_latitude', 'gps_longitude', 'severity', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class AidRequestForm(forms.ModelForm):
    class Meta:
        model = AidRequest
        fields = ['aid_type', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class ShelterForm(forms.ModelForm):
    class Meta:
        model = Shelter
        fields = ['name', 'address', 'gps_latitude', 'gps_longitude', 'capacity', 'contact_person', 'contact_phone', 'special_facilities']

class VolunteerRegistrationForm(forms.ModelForm):
    class Meta:
        model = VolunteerProfile
        fields = ['skills', 'availability_start', 'availability_end', 'emergency_contact_name', 'emergency_contact_phone']
User = get_user_model()
class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = (
        ('CITIZEN', 'Citizen'),
        ('VOLUNTEER', 'Volunteer'),
        ('AUTHORITY', 'Authority'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES)
    phone_number = forms.CharField(max_length=20, required=False)
    address = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role', 'phone_number', 'address']

class DisasterReportFilterForm(forms.Form):
    disaster_type = forms.ChoiceField(choices=[('', 'All Types')] + list(DisasterReport.DISASTER_TYPES), required=False)
    severity = forms.ChoiceField(choices=[('', 'All Severities')] + list(DisasterReport.SEVERITY_LEVELS), required=False)
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    is_verified = forms.ChoiceField(choices=[('', 'All'), ('True', 'Verified'), ('False', 'Unverified')], required=False)    