from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Sponsor, College, SponsorEvent, CollegeEvent

class SponsorRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    contact_no = forms.CharField(max_length=15, required=False)
    address = forms.CharField(max_length=255, required=False)
    state = forms.CharField(max_length=100, required=False)

    class Meta:
        model = Sponsor
        fields = ['username', 'email', 'password1', 'password2', 'contact_no', 'address', 'state']

class CollegeRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    contact_no = forms.CharField(max_length=15, required=False)
    address = forms.CharField(max_length=255, required=False)
    state = forms.CharField(max_length=100, required=False)

    class Meta:
        model = College
        fields = ['username', 'email', 'password1', 'password2', 'contact_no', 'address', 'state']

class SponsorEventForm(forms.ModelForm):
    class Meta:
        model = SponsorEvent
        fields = ['event_name', 'amount', 'keywords', 'location', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'keywords': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Enter keywords separated by commas'}),
        }

class CollegeEventForm(forms.ModelForm):
    class Meta:
        model = CollegeEvent
        fields = ['event_name', 'amount', 'description', 'contact_no', 'basic_deliverables']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'basic_deliverables': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter deliverables separated by commas'}),
        }