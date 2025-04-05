from django.shortcuts import render, redirect
from .models import SponsorListing, ClientListing, Sponsor, College, SponsorEvent, CollegeEvent, EventRequest, SponsorHistory, CollegeSponsorshipHistory
from .forms import SponsorForm, ClientForm, LoginForm, SignupForm, CollegeEventForm, SponsorEventForm
from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
from bson import ObjectId
import json
from datetime import datetime

def sponsor_list(request):
    # Get data from both old and new models
    old_sponsors = SponsorListing.objects.filter(is_active=True)
    new_sponsors = Sponsor.objects.all()
    sponsor_events = SponsorEvent.objects.all()
    
    # Convert old sponsors to match new format
    converted_sponsors = []
    for sponsor in old_sponsors:
        converted_sponsors.append({
            'name': sponsor.name,
            'email': sponsor.contact_email,
            'contact_no': 'N/A',
            'state': 'N/A',
            'avg_rating': 0.0,
            'created_at': sponsor.created_at,
            'description': sponsor.description
        })
    
    # Combine both lists
    all_sponsors = list(new_sponsors) + converted_sponsors
    
    # Get college events for sponsorship opportunities
    college_events = CollegeEvent.objects.all()
    
    # Format events for the template
    events = []
    for event in sponsor_events:
        events.append({
            'id': str(event.id),
            'sponsor_name': event.sponsor_name,
            'description': event.description,
            'amount': event.amount,
            'expected_attendance': event.expected_attendance,
            'deliverables': event.deliverables,
            'keywords': event.keywords,
            'created_at': event.created_at
        })
    
    # Determine what to show based on user type
    user_type = request.session.get('user_type', '')
    is_authenticated = 'user_id' in request.session
    
    return render(request, 'listings/sponsor_list.html', {
        'events': events,
        'user_type': user_type,
        'is_authenticated': is_authenticated
    })

def client_list(request):
    # Get data from both old and new models
    old_clients = ClientListing.objects.filter(is_active=True)
    new_colleges = College.objects.all()
    college_events = CollegeEvent.objects.all()
    
    # Convert old clients to match new format
    converted_colleges = []
    for client in old_clients:
        converted_colleges.append({
            'name': client.event_name,
            'email': client.contact_email,
            'contact_no': 'N/A',
            'state': 'N/A',
            'avg_rating': 0.0,
            'created_at': client.created_at,
            'description': client.description
        })
    
    # Combine both lists
    all_colleges = list(new_colleges) + converted_colleges
    
    return render(request, 'listings/client_list.html', {
        'colleges': all_colleges,
        'college_events': college_events
    })

def create_sponsor(request):
    if request.method == 'POST':
        form = SponsorForm(request.POST)
        if form.is_valid():
            listing = SponsorListing(
                user=request.user,
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                budget=form.cleaned_data['budget'],
                contact_email=form.cleaned_data['contact_email'],
                created_at=datetime.now(),
                is_active=True
            )
            listing.save()
            messages.success(request, 'Sponsor listing created successfully!')
            return redirect('sponsor-list')
    else:
        form = SponsorForm()
    return render(request, 'listings/create_sponsor.html', {'form': form})

def create_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            listing = ClientListing(
                user=request.user,
                event_name=form.cleaned_data['event_name'],
                description=form.cleaned_data['description'],
                required_funding=form.cleaned_data['required_funding'],
                contact_email=form.cleaned_data['contact_email'],
                created_at=datetime.now(),
                is_active=True
            )
            listing.save()
            messages.success(request, 'Client listing created successfully!')
            return redirect('client-list')
    else:
        form = ClientForm()
    return render(request, 'listings/create_client.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user_type = form.cleaned_data['user_type']

            if user_type == 'sponsor':
                try:
                    user = Sponsor.objects.get(email=email)
                    if check_password(password, user.password):
                        # Create JWT tokens with custom claims
                        refresh = RefreshToken()
                        refresh['user_id'] = str(user.id)  # MongoEngine uses id
                        refresh['user_type'] = 'sponsor'
                        refresh['email'] = user.email

                        # Store user info in session
                        request.session['user_id'] = str(user.id)
                        request.session['user_type'] = 'sponsor'
                        request.session['user_name'] = user.name
                        request.session['user_email'] = user.email

                        # Store tokens in session
                        request.session['access_token'] = str(refresh.access_token)
                        request.session['refresh_token'] = str(refresh)

                        messages.success(request, 'Successfully logged in as sponsor!')
                        return redirect('sponsor-list')  # Redirect sponsors to see college events
                except Sponsor.DoesNotExist:
                    pass
            else:
                try:
                    user = College.objects.get(email=email)
                    if check_password(password, user.password):
                        # Create JWT tokens with custom claims
                        refresh = RefreshToken()
                        refresh['user_id'] = str(user.id)  # MongoEngine uses id
                        refresh['user_type'] = 'college'
                        refresh['email'] = user.email

                        # Store user info in session
                        request.session['user_id'] = str(user.id)
                        request.session['user_type'] = 'college'
                        request.session['user_name'] = user.name
                        request.session['user_email'] = user.email

                        # Store tokens in session
                        request.session['access_token'] = str(refresh.access_token)
                        request.session['refresh_token'] = str(refresh)

                        messages.success(request, 'Successfully logged in as college!')
                        return redirect('sponsor-list')  # Redirect colleges to see sponsor events
                except College.DoesNotExist:
                    pass

            messages.error(request, 'Invalid email or password')
    else:
        form = LoginForm()
    return render(request, 'listings/login.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user_type = form.cleaned_data['user_type']
            password = make_password(form.cleaned_data['password'])

            try:
                if user_type == 'sponsor':
                    user = Sponsor(
                        name=form.cleaned_data['name'],
                        email=form.cleaned_data['email'],
                        contact_no=form.cleaned_data['contact_no'],
                        address=form.cleaned_data['address'],
                        state=form.cleaned_data['state'],
                        password=password,
                        created_at=datetime.now()
                    )
                else:
                    user = College(
                        name=form.cleaned_data['name'],
                        email=form.cleaned_data['email'],
                        contact_no=form.cleaned_data['contact_no'],
                        address=form.cleaned_data['address'],
                        state=form.cleaned_data['state'],
                        password=password,
                        created_at=datetime.now()
                    )
                user.save()
                messages.success(request, 'Account created successfully! Please login.')
                return redirect('login')
            except Exception as e:
                messages.error(request, f'Error creating account: {str(e)}')
    else:
        form = SignupForm()
    return render(request, 'listings/signup.html', {'form': form})

def logout(request):
    # Clear the session
    request.session.flush()
    messages.success(request, 'You have been successfully logged out.')
    return redirect('login')

def get_current_user(request):
    if 'user_id' in request.session and 'user_type' in request.session:
        user_id = request.session['user_id']
        user_type = request.session['user_type']
        user_name = request.session.get('user_name', '')
        user_email = request.session.get('user_email', '')

        return JsonResponse({
            'is_authenticated': True,
            'user_id': user_id,
            'user_type': user_type,
            'user_name': user_name,
            'user_email': user_email
        })
    else:
        return JsonResponse({
            'is_authenticated': False
        })

def refresh_token(request):
    if 'refresh_token' in request.session:
        try:
            refresh = RefreshToken(request.session['refresh_token'])
            request.session['access_token'] = str(refresh.access_token)
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'No refresh token found'})

class PricingView(TemplateView):
    template_name = 'listings/pricing.html'

class HomeView(TemplateView):
    template_name = 'listings/home.html'

def add_event(request):
    if 'user_id' not in request.session:
        messages.error(request, 'Please login first')
        return redirect('login')
    
    user_type = request.session.get('user_type')
    if user_type == 'sponsor':
        return render(request, 'listings/add_sponsor_event.html')
    else:
        return render(request, 'listings/add_college_event.html')

def my_requests(request):
    if 'user_id' not in request.session:
        messages.error(request, 'Please login first')
        return redirect('login')
    
    user_id = request.session['user_id']
    user_type = request.session['user_type']
    
    if user_type == 'sponsor':
        requests = EventRequest.objects(sponsor=user_id)
    else:
        requests = EventRequest.objects(college=user_id)
    
    return render(request, 'listings/my_requests.html', {'requests': requests})

def my_history(request):
    if 'user_id' not in request.session:
        messages.error(request, 'Please login first')
        return redirect('login')
    
    user_id = request.session['user_id']
    user_type = request.session['user_type']
    
    if user_type == 'sponsor':
        history = SponsorHistory.objects(sponsor=user_id)
    else:
        history = CollegeSponsorshipHistory.objects(college=user_id)
    
    return render(request, 'listings/my_history.html', {'history': history})

def profile(request):
    if 'user_id' not in request.session:
        messages.error(request, 'Please login first')
        return redirect('login')
    
    user_id = request.session['user_id']
    user_type = request.session['user_type']
    
    if user_type == 'sponsor':
        user = Sponsor.objects.get(id=user_id)
    else:
        user = College.objects.get(id=user_id)
    
    return render(request, 'listings/profile.html', {'user': user})

def settings(request):
    if 'user_id' not in request.session:
        messages.error(request, 'Please login first')
        return redirect('login')
    
    user_id = request.session['user_id']
    user_type = request.session['user_type']
    
    if user_type == 'sponsor':
        user = Sponsor.objects.get(id=user_id)
    else:
        user = College.objects.get(id=user_id)
    
    return render(request, 'listings/settings.html', {'user': user})

@csrf_exempt
def register_interest(request, event_id):
    if 'user_id' not in request.session:
        return JsonResponse({'status': 'error', 'message': 'Please login first'})
    
    try:
        user_id = request.session['user_id']
        user_type = request.session['user_type']
        
        if user_type == 'sponsor':
            event = CollegeEvent.objects.get(id=event_id)
            request = EventRequest(
                sponsor=user_id,
                college=event.college.id,
                event_id=event_id,
                event_type='college_event',
                status='pending',
                price=event.amount,
                basic_deliverables=event.basic_deliverables,
                created_at=datetime.now()
            )
        else:
            event = SponsorEvent.objects.get(id=event_id)
            request = EventRequest(
                college=user_id,
                sponsor=event.sponsor.id,
                event_id=event_id,
                event_type='sponsor_event',
                status='pending',
                price=event.amount,
                basic_deliverables=event.keywords,
                created_at=datetime.now()
            )
        request.save()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

def create_college_event(request):
    if request.method == 'POST':
        form = CollegeEventForm(request.POST)
        if form.is_valid():
            # Get the college from the current user's session
            college_id = request.session.get('user_id')
            try:
                college = College.objects.get(id=college_id)
                
                # Create the new event
                event = CollegeEvent(
                    college=college,
                    event_name=form.cleaned_data['event_name'],
                    amount=form.cleaned_data['amount'],
                    description=form.cleaned_data['description'],
                    contact_no=form.cleaned_data['contact_no'],
                    location=form.cleaned_data['location'],
                    basic_deliverables=form.cleaned_data['basic_deliverables'],
                    created_at=datetime.now()
                )
                event.save()
                
                messages.success(request, 'Event created successfully!')
                return redirect('sponsor-list')
            except College.DoesNotExist:
                messages.error(request, 'College not found. Please log in again.')
                return redirect('login')
    else:
        form = CollegeEventForm()
    
    return render(request, 'listings/create_college_event.html', {'form': form})

def create_sponsor_event(request):
    if request.method == 'POST':
        form = SponsorEventForm(request.POST)
        if form.is_valid():
            # Get the sponsor from the current user's session
            sponsor_id = request.session.get('user_id')
            try:
                sponsor = Sponsor.objects.get(id=sponsor_id)
                
                # Create the new event
                event = SponsorEvent(
                    sponsor=sponsor,
                    sponsor_name=form.cleaned_data['sponsor_name'],
                    description=form.cleaned_data['description'],
                    amount=form.cleaned_data['amount'],
                    expected_attendance=form.cleaned_data['expected_attendance'],
                    deliverables=form.cleaned_data['deliverables'],
                    keywords=form.cleaned_data['keywords'],
                    created_at=datetime.now()
                )
                event.save()
                
                messages.success(request, 'Event created successfully!')
                return redirect('sponsor-list')
            except Sponsor.DoesNotExist:
                messages.error(request, 'Sponsor not found. Please log in again.')
                return redirect('login')
    else:
        form = SponsorEventForm()
    
    return render(request, 'listings/create_sponsor_event.html', {'form': form})