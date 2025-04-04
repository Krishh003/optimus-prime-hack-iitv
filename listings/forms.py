from django import forms
from .models import SponsorListing, ClientListing

class SponsorForm(forms.ModelForm):
    class Meta:
        model = SponsorListing
        fields = ['name', 'description', 'budget', 'contact_email']

class ClientForm(forms.ModelForm):
    class Meta:
        model = ClientListing
        fields = ['event_name', 'description', 'required_funding', 'contact_email']