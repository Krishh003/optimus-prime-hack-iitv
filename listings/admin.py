from django.contrib import admin
from .models import SponsorListing, ClientListing

@admin.register(SponsorListing)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ('name', 'budget', 'contact_email', 'created_at')

@admin.register(ClientListing)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'required_funding', 'contact_email', 'created_at')