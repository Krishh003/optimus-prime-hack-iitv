from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Sponsor, College, SponsorEvent, CollegeEvent, EventRequest, SponsorHistory, CollegeSponsorshipHistory, EVENT_TYPE_CHOICES
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

def sponsor_dashboard(request):
    # Get filter parameters
    event_type = request.GET.get('event_type')
    budget = request.GET.get('budget')
    state = request.GET.get('state')
    
    # Create some dummy data for display
    events = [
        {
            'id': 1,
            'event_name': 'Tech Fest 2025',
            'college': {'username': 'IIT Bombay', 'college_photo': None},
            'event_type': 'technical',
            'amount': 50000,
            'description': 'Annual technical festival with competitions, workshops, and exhibitions.',
            'basic_deliverables': 'Logo on banners, Social media promotion, Stage mention',
            'created_at': '2025-04-01'
        },
        {
            'id': 2,
            'event_name': 'Cultural Night',
            'college': {'username': 'Delhi University', 'college_photo': None},
            'event_type': 'cultural',
            'amount': 30000,
            'description': 'A grand cultural evening featuring music, dance, and theatrical performances.',
            'basic_deliverables': 'Brand placement, VIP passes, Marketing rights',
            'created_at': '2025-04-02'
        },
        {
            'id': 3,
            'event_name': 'Sports Meet 2025',
            'college': {'username': 'NIT Trichy', 'college_photo': None},
            'event_type': 'sports',
            'amount': 40000,
            'description': 'Inter-college sports competition with multiple sporting events.',
            'basic_deliverables': 'Jersey branding, Ground displays, Award ceremony presence',
            'created_at': '2025-04-03'
        }
    ]
    
    context = {
        'events': events,
        'filters': {
            'event_type': event_type,
            'budget': budget,
            'state': state,
        }
    }
    return render(request, 'listings/sponsor_dashboard.html', context)

@login_required
def college_dashboard(request):
    if not isinstance(request.user, Sponsor) or not request.user.is_college:
        messages.error(request, 'Access denied. Please login as a college.')
        return redirect('home')
    
    events = CollegeEvent.objects.filter(college=request.user)
    return render(request, 'listings/college_dashboard.html', {'events': events})

@login_required
def create_sponsor_event(request):
    if not hasattr(request.user, 'sponsor'):
        messages.error(request, "Only sponsors can create events.")
        return redirect('home')
    
    if request.method == 'POST':
        event_name = request.POST.get('event_name')
        event_type = request.POST.get('event_type')
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        deliverables = request.POST.getlist('deliverables[]')
        
        try:
            # Create the sponsor event
            sponsor_event = SponsorEvent.objects.create(
                sponsor=request.user.sponsor,
                event_name=event_name,
                event_type=event_type,
                amount=amount,
                description=description,
                basic_deliverables=", ".join(deliverables)
            )
            messages.success(request, "Sponsorship opportunity created successfully!")
            return redirect('sdashboard')
        except Exception as e:
            messages.error(request, f"Error creating event: {str(e)}")
            return render(request, 'listings/create_sponsor_event.html')
    
    return render(request, 'listings/create_sponsor_event.html')

@login_required
def create_college_event(request):
    if not request.user.is_college:
        messages.error(request, "Only colleges can create events.")
        return redirect('home')
    
    if request.method == 'POST':
        try:
            event = CollegeEvent.objects.create(
                college=request.user,
                event_name=request.POST['event_name'],
                event_type=request.POST['event_type'],
                amount=request.POST['amount'],
                description=request.POST['description'],
                contact_no=request.POST.get('contact_no', ''),
                basic_deliverables=request.POST['basic_deliverables']
            )
            messages.success(request, "Event created successfully!")
            return redirect('college_dashboard')
        except Exception as e:
            messages.error(request, f"Error creating event: {str(e)}")
    
    context = {
        'form': {'fields': {'event_type': {'choices': EVENT_TYPE_CHOICES}}}
    }
    return render(request, 'listings/create_college_event.html', context)

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

def sdashboard(request):
    # Create some dummy data for display
    now = timezone.now()
    events = [
        {
            'id': 1,
            'event_name': 'Tech Fest 2025',
            'college': {'username': 'IIT Bombay', 'college_photo': None},
            'event_type': 'technical',
            'amount': 50000,
            'description': 'Annual technical festival with competitions, workshops, and exhibitions.',
            'basic_deliverables': 'Logo on banners, Social media promotion, Stage mention',
            'created_at': now - timedelta(days=2)
        },
        {
            'id': 2,
            'event_name': 'Cultural Night',
            'college': {'username': 'Delhi University', 'college_photo': None},
            'event_type': 'cultural',
            'amount': 30000,
            'description': 'A grand cultural evening featuring music, dance, and theatrical performances.',
            'basic_deliverables': 'Brand placement, VIP passes, Marketing rights',
            'created_at': now - timedelta(days=1)
        },
        {
            'id': 3,
            'event_name': 'Sports Meet 2025',
            'college': {'username': 'NIT Trichy', 'college_photo': None},
            'event_type': 'sports',
            'amount': 40000,
            'description': 'Inter-college sports competition with multiple sporting events.',
            'basic_deliverables': 'Jersey branding, Ground displays, Award ceremony presence',
            'created_at': now - timedelta(hours=12)
        }
    ]
    
    context = {
        'events': events,
    }
    return render(request, 'listings/sdashboard.html', context)