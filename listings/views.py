from django.shortcuts import render, redirect
from .models import Sponsor, College, SponsorEvent, CollegeEvent
from .forms import SponsorForm, ClientForm
from django.contrib import messages
from django.views.generic import TemplateView

def sponsor_list(request):
    sponsors = Sponsor.objects.all()
    sponsor_events = SponsorEvent.objects.all()
    return render(request, 'listings/sponsor_list.html', {
        'sponsors': sponsors,
        'sponsor_events': sponsor_events
    })

def client_list(request):
    colleges = College.objects.all()
    college_events = CollegeEvent.objects.all()
    return render(request, 'listings/client_list.html', {
        'colleges': colleges,
        'college_events': college_events
    })

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