from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Sponsor, College, SponsorEvent, CollegeEvent, EventRequest, SponsorHistory, CollegeSponsorshipHistory
from .forms import SponsorRegistrationForm, CollegeRegistrationForm, SponsorEventForm, CollegeEventForm

def home(request):
    return render(request, 'listings/home.html')

def register_sponsor(request):
    if request.method == 'POST':
        form = SponsorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('sponsor_dashboard')
    else:
        form = SponsorRegistrationForm()
    return render(request, 'listings/register_sponsor.html', {'form': form})

def register_college(request):
    if request.method == 'POST':
        form = CollegeRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('college_dashboard')
    else:
        form = CollegeRegistrationForm()
    return render(request, 'listings/register_college.html', {'form': form})

@login_required
def sponsor_dashboard(request):
    if not isinstance(request.user, Sponsor):
        messages.error(request, 'Access denied. Please login as a sponsor.')
        return redirect('home')
    
    events = CollegeEvent.objects.all()
    return render(request, 'listings/sponsor_dashboard.html', {'events': events})

@login_required
def college_dashboard(request):
    if not isinstance(request.user, College):
        messages.error(request, 'Access denied. Please login as a college.')
        return redirect('home')
    
    events = CollegeEvent.objects.filter(college=request.user)
    return render(request, 'listings/college_dashboard.html', {'events': events})

@login_required
def create_sponsor_event(request):
    if not isinstance(request.user, Sponsor):
        messages.error(request, 'Access denied. Please login as a sponsor.')
        return redirect('home')
    
    if request.method == 'POST':
        form = SponsorEventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.sponsor = request.user
            event.save()
            messages.success(request, 'Event created successfully!')
            return redirect('sponsor_dashboard')
    else:
        form = SponsorEventForm()
    return render(request, 'listings/create_sponsor_event.html', {'form': form})

@login_required
def create_college_event(request):
    if not isinstance(request.user, College):
        messages.error(request, 'Access denied. Please login as a college.')
        return redirect('home')
    
    if request.method == 'POST':
        form = CollegeEventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.college = request.user
            event.save()
            messages.success(request, 'Event created successfully!')
            return redirect('college_dashboard')
    else:
        form = CollegeEventForm()
    return render(request, 'listings/create_college_event.html', {'form': form})

@login_required
def send_event_request(request, event_id):
    if not isinstance(request.user, Sponsor):
        messages.error(request, 'Access denied. Please login as a sponsor.')
        return redirect('home')
    
    event = get_object_or_404(CollegeEvent, id=event_id)
    
    if request.method == 'POST':
        # Check if request already exists
        existing_request = EventRequest.objects.filter(
            sponsor=request.user,
            event=event
        ).first()
        
        if existing_request:
            messages.warning(request, 'You have already sent a request for this event.')
        else:
            EventRequest.objects.create(
                sponsor=request.user,
                college=event.college,
                event=event,
                event_type='college_event',
                price=event.amount,
                basic_deliverables=event.basic_deliverables
            )
            messages.success(request, 'Your interest has been sent to the college.')
    
    return redirect('sponsor_dashboard')

@login_required
def my_requests(request):
    if isinstance(request.user, Sponsor):
        requests = EventRequest.objects.filter(sponsor=request.user)
        template = 'listings/sponsor_requests.html'
    else:
        requests = EventRequest.objects.filter(college=request.user)
        template = 'listings/college_requests.html'
    
    return render(request, template, {'requests': requests})

@login_required
def my_history(request):
    if isinstance(request.user, Sponsor):
        history = SponsorHistory.objects.filter(sponsor=request.user)
        template = 'listings/sponsor_history.html'
    else:
        history = CollegeSponsorshipHistory.objects.filter(college=request.user)
        template = 'listings/college_history.html'
    
    return render(request, template, {'history': history})