from django.shortcuts import render, redirect
from .models import SponsorListing, ClientListing
from .forms import SponsorForm, ClientForm
from django.contrib import messages
from django.views.generic import TemplateView

def sponsor_list(request):
    sponsors = SponsorListing.objects.filter(is_active=True)
    return render(request, 'listings/sponsor_list.html', {'sponsors': sponsors})

def client_list(request):
    clients = ClientListing.objects.filter(is_active=True)
    return render(request, 'listings/client_list.html', {'clients': clients})

def create_sponsor(request):
    if request.method == 'POST':
        form = SponsorForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.is_active = True  # Set to False if payment required
            instance.save()
            messages.success(request, 'Sponsor listing created successfully!')
            return redirect('sponsor-list')
    else:
        form = SponsorForm()
    return render(request, 'listings/create_sponsor.html', {'form': form})

def create_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.is_active = True  # Set to False if payment required
            instance.save()
            messages.success(request, 'Client listing created successfully!')
            return redirect('client-list')
    else:
        form = ClientForm()
    return render(request, 'listings/create_client.html', {'form': form})

class PricingView(TemplateView):
    template_name = 'listings/pricing.html'

class HomeView(TemplateView):
    template_name = 'listings/home.html'