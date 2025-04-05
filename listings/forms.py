from django import forms
from .models import SponsorListing, ClientListing, Sponsor, College
from listings.models import CollegeEvent

class SponsorForm(forms.Form):
    name = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    budget = forms.DecimalField(max_digits=10, decimal_places=2)
    contact_email = forms.EmailField()

class ClientForm(forms.Form):
    event_name = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    required_funding = forms.DecimalField(max_digits=10, decimal_places=2)
    contact_email = forms.EmailField()

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    user_type = forms.ChoiceField(choices=[('sponsor', 'Sponsor'), ('college', 'College')])

class SignupForm(forms.Form):
    name = forms.CharField(max_length=255)
    email = forms.EmailField()
    contact_no = forms.CharField(max_length=15)
    address = forms.CharField(max_length=255)
    state = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    user_type = forms.ChoiceField(choices=[('sponsor', 'Sponsor'), ('college', 'College')])

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

class CollegeEventForm(forms.Form):
    event_name = forms.CharField(max_length=200, required=True)
    amount = forms.IntegerField(required=True)
    description = forms.CharField(widget=forms.Textarea, required=True)
    contact_no = forms.CharField(max_length=15, required=True)
    location = forms.CharField(max_length=200, required=True)
    basic_deliverables = forms.CharField(
        widget=forms.Textarea,
        required=True,
        help_text="Enter deliverables separated by commas"
    )

class SponsorEventForm(forms.Form):
    sponsor_name = forms.CharField(max_length=255, required=True)
    description = forms.CharField(widget=forms.Textarea, required=True)
    amount = forms.IntegerField(required=True)
    expected_attendance = forms.CharField(max_length=100, required=True)
    deliverables = forms.CharField(
        widget=forms.Textarea,
        required=True,
        help_text="Enter deliverables separated by commas"
    )
    keywords = forms.CharField(
        widget=forms.Textarea,
        required=True,
        help_text="Enter keywords separated by commas (e.g., Technology, Innovation, Networking)"
    )