from django import forms
from .models import SponsorListing, ClientListing, Sponsor, College

class SponsorForm(forms.ModelForm):
    class Meta:
        model = SponsorListing
        fields = ['name', 'description', 'budget', 'contact_email']

class ClientForm(forms.ModelForm):
    class Meta:
        model = ClientListing
        fields = ['event_name', 'description', 'required_funding', 'contact_email']

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

class CollegeForm(forms.Form):
    pass
