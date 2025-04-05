from django.shortcuts import render, redirect
from .models import SponsorListing, ClientListing, Sponsor, College, SponsorEvent, CollegeEvent, EventRequest, SponsorHistory, CollegeSponsorshipHistory, Admin, Chat
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
from django.views.decorators.http import require_POST

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
    # Get college events for sponsorship opportunities
    college_events = CollegeEvent.objects.all()
    
    # Format events for the template
    events = []
    for event in college_events:
        events.append({
            'id': str(event.id),
            'event_name': event.event_name,
            'description': event.description,
            'amount': event.amount,
            'contact_no': event.contact_no,
            'location': event.location,
            'basic_deliverables': event.basic_deliverables,
            'created_at': event.created_at
        })
    
    # Determine what to show based on user type
    user_type = request.session.get('user_type', '')
    is_authenticated = 'user_id' in request.session
    
    return render(request, 'listings/client_list.html', {
        'events': events,
        'user_type': user_type,
        'is_authenticated': is_authenticated
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

            if user_type == 'admin':
                try:
                    admin = Admin.objects.get(email=email)
                    if check_password(password, admin.password):
                        # Store admin info in session
                        request.session['user_id'] = str(admin.id)
                        request.session['user_type'] = 'admin'
                        request.session['user_name'] = admin.username
                        request.session['user_email'] = admin.email

                        messages.success(request, 'Successfully logged in as admin!')
                        return redirect('admin-dashboard')
                    else:
                        messages.error(request, 'Invalid password')
                except Admin.DoesNotExist:
                    messages.error(request, 'Admin account not found')
                return redirect('login')

            elif user_type == 'sponsor':
                try:
                    user = Sponsor.objects.get(email=email)
                    if check_password(password, user.password):
                        # Create JWT tokens with custom claims
                        refresh = RefreshToken()
                        refresh['user_id'] = str(user.id)
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
                        return redirect('sponsor-list')
                    else:
                        messages.error(request, 'Invalid password')
                except Sponsor.DoesNotExist:
                    messages.error(request, 'Sponsor account not found')
                return redirect('login')
            else:
                try:
                    user = College.objects.get(email=email)
                    if check_password(password, user.password):
                        # Create JWT tokens with custom claims
                        refresh = RefreshToken()
                        refresh['user_id'] = str(user.id)
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
                        return redirect('sponsor-list')
                    else:
                        messages.error(request, 'Invalid password')
                except College.DoesNotExist:
                    messages.error(request, 'College account not found')
                return redirect('login')
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
        return redirect('create-sponsor-event')
    else:
        return redirect('create-college-event')

def my_requests(request):
    if 'user_id' not in request.session:
        messages.error(request, 'Please login first')
        return redirect('login')
    
    user_id = request.session['user_id']
    user_type = request.session['user_type']
    
    # Initialize separate lists for created and received requests
    created_requests = []
    received_requests = []
    accepted_requests = []
    
    if user_type == 'sponsor':
        try:
            # Get requests for the sponsor's events (created by sponsor)
            sponsor_events = SponsorEvent.objects(sponsor=user_id)
            event_ids = [str(event.id) for event in sponsor_events]
            created_requests = EventRequest.objects(event_id__in=event_ids, event_type='sponsor_event')
            
            # Get requests made by the sponsor to college events
            received_requests = EventRequest.objects(sponsor=user_id)
            
            # Get accepted requests for the sponsor's events
            accepted_requests = EventRequest.objects(event_id__in=event_ids, event_type='sponsor_event', status='accepted')
        except Exception as e:
            print(f"Error fetching sponsor requests: {str(e)}")
            messages.error(request, 'Error fetching your requests. Please try again.')
    else:
        try:
            # Get requests made by the college to sponsor events
            created_requests = EventRequest.objects(college=user_id)
            
            # Get requests for the college's events (received by college)
            college_events = CollegeEvent.objects(college=user_id)
            event_ids = [str(event.id) for event in college_events]
            received_requests = EventRequest.objects(event_id__in=event_ids, event_type='college_event')
            
            # Get accepted requests for the college's events
            accepted_requests = EventRequest.objects(event_id__in=event_ids, event_type='college_event', status='accepted')
        except Exception as e:
            print(f"Error fetching college requests: {str(e)}")
            messages.error(request, 'Error fetching your requests. Please try again.')
    
    def process_requests(requests_list):
        processed_requests = []
        for req in requests_list:
            try:
                # Skip if event_id is not a valid ObjectId
                if not req.event_id or len(req.event_id) != 24:
                    print(f"Skipping request {req.id} - Invalid event_id format: {req.event_id}")
                    continue
                
                # Get event details based on event type
                event_name = "Event no longer available"
                event_exists = True
                
                if req.event_type == 'sponsor_event':
                    try:
                        event = SponsorEvent.objects.get(id=req.event_id)
                        event_name = event.sponsor_name
                    except SponsorEvent.DoesNotExist:
                        print(f"SponsorEvent not found for id: {req.event_id} (Request ID: {req.id})")
                        event_exists = False
                else:
                    try:
                        event = CollegeEvent.objects.get(id=req.event_id)
                        event_name = event.event_name
                    except CollegeEvent.DoesNotExist:
                        print(f"CollegeEvent not found for id: {req.event_id} (Request ID: {req.id})")
                        event_exists = False
                
                # Get college/sponsor details
                try:
                    if user_type == 'sponsor':
                        college = College.objects.get(id=req.college.id) if req.college else None
                        other_party = {
                            'id': str(college.id) if college else None,
                            'name': college.name if college else 'Unknown College',
                            'email': college.email if college else 'N/A'
                        }
                    else:
                        sponsor = Sponsor.objects.get(id=req.sponsor.id) if req.sponsor else None
                        other_party = {
                            'id': str(sponsor.id) if sponsor else None,
                            'name': sponsor.name if sponsor else 'Unknown Sponsor',
                            'email': sponsor.email if sponsor else 'N/A'
                        }
                except Exception as e:
                    print(f"Error getting other party details: {str(e)}")
                    other_party = {
                        'id': None,
                        'name': 'Unknown',
                        'email': 'N/A'
                    }
                
                processed_requests.append({
                    'id': str(req.id),
                    'event_id': req.event_id,
                    'event_name': event_name,
                    'event_type': req.event_type,
                    'status': req.status,
                    'price': req.price,
                    'created_at': req.created_at,
                    'other_party': other_party,
                    'event_exists': event_exists
                })
            except Exception as e:
                print(f"Error processing request {req.id}: {str(e)}")
                continue
        
        return processed_requests
    
    # Process all request lists
    processed_created = process_requests(created_requests)
    processed_received = process_requests(received_requests)
    processed_accepted = process_requests(accepted_requests)
    
    return render(request, 'listings/my_requests.html', {
        'created_requests': processed_created,
        'received_requests': processed_received,
        'accepted_requests': processed_accepted,
        'user_type': user_type
    })

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
        events = SponsorEvent.objects(sponsor=user_id)
    else:
        user = College.objects.get(id=user_id)
        events = CollegeEvent.objects(college=user_id)
    
    return render(request, 'listings/profile.html', {
        'user': user,
        'events': events
    })

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
    if request.method == 'POST':
        try:
            user_id = request.session.get('user_id')
            user_type = request.session.get('user_type')
            
            if not user_id or not user_type:
                return JsonResponse({'error': 'User not authenticated'}, status=401)
            
            # Try to get the event from both sponsor and college events
            try:
                event = SponsorEvent.objects.get(id=event_id)
                event_type = 'sponsor_event'
            except SponsorEvent.DoesNotExist:
                try:
                    event = CollegeEvent.objects.get(id=event_id)
                    event_type = 'college_event'
                except CollegeEvent.DoesNotExist:
                    return JsonResponse({'error': 'Event not found'}, status=404)
            
            # Create a new event request
            event_request = EventRequest(
                sponsor=Sponsor.objects.get(id=user_id) if user_type == 'sponsor' else None,
                college=College.objects.get(id=user_id) if user_type == 'college' else None,
                event_id=str(event_id),
                event_type=event_type,
                status='pending',
                price=event.amount,
                basic_deliverables=event.deliverables if event_type == 'sponsor_event' else event.basic_deliverables,
                created_at=datetime.now()
            )
            event_request.save()
            
            return JsonResponse({'message': 'Interest registered successfully'})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)

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

def create_default_admin():
    try:
        # Check if default admin exists
        admin = Admin.objects.get(username='admin')
        print("Default admin account already exists")
        return admin
    except Admin.DoesNotExist:
        # Create default admin
        admin = Admin(
            username='admin',
            email='admin@example.com',
            password=make_password('admin@123'),
            created_at=datetime.now()
        )
        try:
            admin.save()
            print("Created default admin account with username: admin and password: admin@123")
            return admin
        except Exception as e:
            print(f"Error creating default admin: {str(e)}")
            return None

def create_admin(request):
    if request.method == 'POST':
        if request.session.get('user_type') != 'admin':
            messages.error(request, 'Only admins can create other admin accounts')
            return redirect('login')
        
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            admin = Admin(
                username=username,
                email=email,
                password=make_password(password),
                created_at=datetime.now(),
                created_by=Admin.objects.get(id=request.session['user_id'])
            )
            admin.save()
            messages.success(request, 'Admin account created successfully!')
            return redirect('admin-list')
        except Exception as e:
            messages.error(request, f'Error creating admin account: {str(e)}')
    
    return render(request, 'listings/create_admin.html')

def admin_list(request):
    if request.session.get('user_type') != 'admin':
        messages.error(request, 'Only admins can view this page')
        return redirect('login')
    
    admins = Admin.objects.all()
    return render(request, 'listings/admin_list.html', {'admins': admins})

def delete_admin(request, admin_id):
    if request.session.get('user_type') != 'admin':
        messages.error(request, 'Only admins can delete admin accounts')
        return redirect('login')
    
    try:
        admin = Admin.objects.get(id=admin_id)
        if admin.username == 'admin':
            messages.error(request, 'Cannot delete the default admin account')
        else:
            admin.delete()
            messages.success(request, 'Admin account deleted successfully!')
    except Admin.DoesNotExist:
        messages.error(request, 'Admin account not found')
    
    return redirect('admin-list')

def admin_dashboard(request):
    # Check if user is logged in as admin
    if request.session.get('user_type') != 'admin':
        messages.error(request, 'You must be logged in as an admin to access this page')
        return redirect('login')
    
    # Get statistics for the dashboard
    total_sponsors = Sponsor.objects.count()
    total_colleges = College.objects.count()
    total_events = CollegeEvent.objects.count() + SponsorEvent.objects.count()
    pending_requests = EventRequest.objects.filter(status='pending').count()
    
    context = {
        'total_sponsors': total_sponsors,
        'total_colleges': total_colleges,
        'total_events': total_events,
        'pending_requests': pending_requests
    }
    
    return render(request, 'listings/admin_dashboard.html', context)

@csrf_exempt
def cancel_request(request, request_id):
    if request.method == 'POST':
        try:
            user_id = request.session.get('user_id')
            user_type = request.session.get('user_type')
            
            if not user_id or not user_type:
                return JsonResponse({'error': 'User not authenticated'}, status=401)
            
            # Get the request
            try:
                event_request = EventRequest.objects.get(id=request_id)
                
                # Verify the user owns this request
                if user_type == 'sponsor' and str(event_request.sponsor.id) != user_id:
                    return JsonResponse({'error': 'Unauthorized'}, status=403)
                elif user_type == 'college' and str(event_request.college.id) != user_id:
                    return JsonResponse({'error': 'Unauthorized'}, status=403)
                
                # Only allow canceling pending requests
                if event_request.status != 'pending':
                    return JsonResponse({'error': 'Can only cancel pending requests'}, status=400)
                
                # Update the request status
                event_request.status = 'rejected'
                event_request.save()
                
                return JsonResponse({'message': 'Request cancelled successfully'})
                
            except EventRequest.DoesNotExist:
                return JsonResponse({'error': 'Request not found'}, status=404)
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def request_details(request, request_id):
    if 'user_id' not in request.session:
        messages.error(request, 'Please login first')
        return redirect('login')
    
    try:
        user_id = request.session['user_id']
        user_type = request.session['user_type']
        
        # Get the request
        event_request = EventRequest.objects.get(id=request_id)
        
        # Verify the user owns this request
        if user_type == 'sponsor' and str(event_request.sponsor.id) != user_id:
            messages.error(request, 'Unauthorized access')
            return redirect('my_requests')
        elif user_type == 'college' and str(event_request.college.id) != user_id:
            messages.error(request, 'Unauthorized access')
            return redirect('my_requests')
        
        # Get event data
        if event_request.event_type == 'sponsor_event':
            event = SponsorEvent.objects.get(id=event_request.event_id)
            event_data = {
                'name': event.sponsor_name,
                'description': event.description,
                'amount': event.amount,
                'expected_attendance': event.expected_attendance,
                'deliverables': event.deliverables,
                'keywords': event.keywords,
                'created_at': event.created_at
            }
        else:
            event = CollegeEvent.objects.get(id=event_request.event_id)
            event_data = {
                'name': event.event_name,
                'description': event.description,
                'amount': event.amount,
                'contact_no': event.contact_no,
                'location': event.location,
                'basic_deliverables': event.basic_deliverables,
                'created_at': event.created_at
            }
        
        # Add status color for the badge
        status_color = {
            'pending': 'warning',
            'accepted': 'success',
            'rejected': 'danger'
        }.get(event_request.status, 'secondary')
        
        request_data = {
            'id': str(event_request.id),
            'event': event_data,
            'status': event_request.status.capitalize(),
            'status_color': status_color,
            'amount': event_request.price,
            'created_at': event_request.created_at,
            'message': event_request.basic_deliverables
        }
        
        return render(request, 'listings/request_details.html', {
            'request': request_data,
            'user_type': user_type
        })
        
    except EventRequest.DoesNotExist:
        messages.error(request, 'Request not found')
        return redirect('my_requests')
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        return redirect('my_requests')

@csrf_exempt
def accept_request(request, request_id):
    if 'user_id' not in request.session:
        messages.error(request, 'Please login first')
        return redirect('login')
    
    try:
        # Validate request_id format
        if not request_id or len(request_id) != 24:
            messages.error(request, 'Invalid request ID')
            return redirect('my_requests')
            
        event_request = EventRequest.objects.get(id=ObjectId(request_id))
        user_id = request.session['user_id']
        user_type = request.session['user_type']
        
        # Check if the user has permission to accept this request
        if user_type == 'sponsor':
            if not event_request.sponsor or str(event_request.sponsor.id) != user_id:
                messages.error(request, 'You do not have permission to accept this request')
                return redirect('my_requests')
        else:
            if not event_request.college or str(event_request.college.id) != user_id:
                messages.error(request, 'You do not have permission to accept this request')
                return redirect('my_requests')
        
        # Update request status
        event_request.status = 'accepted'
        event_request.save()
        
        # Create history records
        try:
            if user_type == 'sponsor':
                SponsorHistory(
                    sponsor=event_request.sponsor,
                    college=event_request.college,
                    event_id=event_request.event_id,
                    event_type=event_request.event_type,
                    amount=event_request.price,
                    created_at=datetime.now()
                ).save()
            else:
                CollegeSponsorshipHistory(
                    college=event_request.college,
                    sponsor=event_request.sponsor,
                    event_id=event_request.event_id,
                    event_type=event_request.event_type,
                    amount=event_request.price,
                    created_at=datetime.now()
                ).save()
        except Exception as e:
            print(f"Error creating history record: {str(e)}")
            # Continue even if history creation fails
        
        # Create initial chat message
        try:
            initial_message = f"Request accepted! Let's discuss the details."
            chat = Chat(
                request=event_request,
                message=initial_message,
                created_at=datetime.now()
            )
            
            if user_type == 'sponsor':
                chat.sender = event_request.sponsor
                chat.receiver = event_request.college
            else:
                chat.sender = event_request.college
                chat.receiver = event_request.sponsor
                
            chat.save()
        except Exception as e:
            print(f"Error creating chat message: {str(e)}")
            # Continue even if chat creation fails
        
        messages.success(request, 'Request accepted successfully!')
        return redirect('my_requests')
        
    except EventRequest.DoesNotExist:
        messages.error(request, 'Request not found')
        return redirect('my_requests')
    except Exception as e:
        print(f"Error accepting request: {str(e)}")
        messages.error(request, 'An error occurred while accepting the request')
        return redirect('my_requests')

@csrf_exempt
def chat_view(request, request_id):
    if 'user_id' not in request.session:
        messages.error(request, 'Please login first')
        return redirect('login')
    
    try:
        event_request = EventRequest.objects.get(id=ObjectId(request_id))
        user_id = request.session['user_id']
        user_type = request.session['user_type']
        
        # Get the other party's information
        if user_type == 'sponsor':
            other_party = College.objects.get(id=event_request.college.id)
        else:
            other_party = Sponsor.objects.get(id=event_request.sponsor.id)
        
        return render(request, 'listings/chat.html', {
            'request_id': request_id,
            'other_party': other_party,
            'user_id': user_id,
            'user_type': user_type
        })
    except (EventRequest.DoesNotExist, Sponsor.DoesNotExist, College.DoesNotExist):
        messages.error(request, 'Invalid request')
        return redirect('my_requests')

@csrf_exempt
@require_POST
def send_message(request, request_id):
    if 'user_id' not in request.session:
        return JsonResponse({'error': 'Please login first'}, status=401)
    
    try:
        data = json.loads(request.body)
        message_text = data.get('message')
        
        if not message_text:
            return JsonResponse({'error': 'Message cannot be empty'}, status=400)
        
        event_request = EventRequest.objects.get(id=ObjectId(request_id))
        user_id = request.session['user_id']
        user_type = request.session['user_type']
        
        # Create new chat message
        chat = Chat(
            request=event_request,
            message=message_text,
            created_at=datetime.now()
        )
        
        if user_type == 'sponsor':
            chat.sender = Sponsor.objects.get(id=user_id)
            chat.receiver = event_request.college
        else:
            chat.sender = College.objects.get(id=user_id)
            chat.receiver = event_request.sponsor
        
        chat.save()
        
        return JsonResponse({
            'id': str(chat.id),
            'message': chat.message,
            'created_at': chat.created_at.isoformat(),
            'sender': {
                'id': str(chat.sender.id),
                'name': chat.sender.name
            }
        })
    except (EventRequest.DoesNotExist, Sponsor.DoesNotExist, College.DoesNotExist):
        return JsonResponse({'error': 'Invalid request'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_messages(request, request_id):
    if 'user_id' not in request.session:
        return JsonResponse({'error': 'Please login first'}, status=401)
    
    try:
        event_request = EventRequest.objects.get(id=ObjectId(request_id))
        messages = Chat.objects.filter(request=event_request).order_by('created_at')
        
        message_list = []
        for msg in messages:
            # Handle the case where sender might be an ObjectId or a Document
            sender_id = None
            sender_name = 'System'
            
            if msg.sender:
                if isinstance(msg.sender, (Sponsor, College)):
                    sender_id = str(msg.sender.id)
                    sender_name = msg.sender.name
                else:
                    # If sender is an ObjectId, try to fetch the actual document
                    try:
                        # Try Sponsor first
                        sender = Sponsor.objects.get(id=msg.sender)
                        sender_id = str(sender.id)
                        sender_name = sender.name
                    except Sponsor.DoesNotExist:
                        try:
                            # Try College if Sponsor not found
                            sender = College.objects.get(id=msg.sender)
                            sender_id = str(sender.id)
                            sender_name = sender.name
                        except College.DoesNotExist:
                            # If neither found, use default values
                            sender_id = str(msg.sender)
                            sender_name = 'Unknown'
            
            message_list.append({
                'id': str(msg.id),
                'message': msg.message,
                'created_at': msg.created_at.isoformat(),
                'sender': {
                    'id': sender_id,
                    'name': sender_name
                }
            })
        
        return JsonResponse(message_list, safe=False)
    except (EventRequest.DoesNotExist, Sponsor.DoesNotExist, College.DoesNotExist):
        return JsonResponse({'error': 'Invalid request'}, status=400)
    except Exception as e:
        print(f"Error in get_messages: {str(e)}")  # Add logging
        return JsonResponse({'error': 'An error occurred while fetching messages'}, status=500)

def event_details(request, event_id):
    if 'user_id' not in request.session:
        messages.error(request, 'Please login first')
        return redirect('login')
    
    try:
        user_id = request.session['user_id']
        user_type = request.session['user_type']
        
        # Try to get the event from both sponsor and college events
        try:
            event = SponsorEvent.objects.get(id=event_id)
            event_type = 'sponsor_event'
        except SponsorEvent.DoesNotExist:
            event = CollegeEvent.objects.get(id=event_id)
            event_type = 'college_event'
        
        # Verify the user owns this event
        if (user_type == 'sponsor' and str(event.sponsor.id) != user_id) or \
           (user_type == 'college' and str(event.college.id) != user_id):
            messages.error(request, 'Unauthorized access')
            return redirect('profile')
        
        # Format event data for template
        event_data = {
            'id': str(event.id),
            'name': event.sponsor_name if event_type == 'sponsor_event' else event.event_name,
            'description': event.description,
            'amount': event.amount,
            'created_at': event.created_at,
            'type': event_type
        }
        
        if event_type == 'sponsor_event':
            event_data.update({
                'expected_attendance': event.expected_attendance,
                'deliverables': event.deliverables,
                'keywords': event.keywords
            })
        else:
            event_data.update({
                'contact_no': event.contact_no,
                'location': event.location,
                'basic_deliverables': event.basic_deliverables
            })
        
        return render(request, 'listings/event_details.html', {
            'event': event_data,
            'user_type': user_type
        })
        
    except (SponsorEvent.DoesNotExist, CollegeEvent.DoesNotExist):
        messages.error(request, 'Event not found')
        return redirect('profile')
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        return redirect('profile')

def edit_event(request, event_id):
    if 'user_id' not in request.session:
        messages.error(request, 'Please login first')
        return redirect('login')
    
    try:
        user_id = request.session['user_id']
        user_type = request.session['user_type']
        
        # Try to get the event from both sponsor and college events
        try:
            event = SponsorEvent.objects.get(id=event_id)
            event_type = 'sponsor_event'
            form_class = SponsorEventForm
        except SponsorEvent.DoesNotExist:
            event = CollegeEvent.objects.get(id=event_id)
            event_type = 'college_event'
            form_class = CollegeEventForm
        
        # Verify the user owns this event
        if (user_type == 'sponsor' and str(event.sponsor.id) != user_id) or \
           (user_type == 'college' and str(event.college.id) != user_id):
            messages.error(request, 'Unauthorized access')
            return redirect('profile')
        
        if request.method == 'POST':
            form = form_class(request.POST)
            if form.is_valid():
                if event_type == 'sponsor_event':
                    event.sponsor_name = form.cleaned_data['sponsor_name']
                    event.description = form.cleaned_data['description']
                    event.amount = form.cleaned_data['amount']
                    event.expected_attendance = form.cleaned_data['expected_attendance']
                    event.deliverables = form.cleaned_data['deliverables']
                    event.keywords = form.cleaned_data['keywords']
                else:
                    event.event_name = form.cleaned_data['event_name']
                    event.description = form.cleaned_data['description']
                    event.amount = form.cleaned_data['amount']
                    event.contact_no = form.cleaned_data['contact_no']
                    event.location = form.cleaned_data['location']
                    event.basic_deliverables = form.cleaned_data['basic_deliverables']
                
                event.save()
                messages.success(request, 'Event updated successfully!')
                return redirect('event_details', event_id=event_id)
        else:
            # Initialize form with current event data
            if event_type == 'sponsor_event':
                initial_data = {
                    'sponsor_name': event.sponsor_name,
                    'description': event.description,
                    'amount': event.amount,
                    'expected_attendance': event.expected_attendance,
                    'deliverables': event.deliverables,
                    'keywords': event.keywords
                }
            else:
                initial_data = {
                    'event_name': event.event_name,
                    'description': event.description,
                    'amount': event.amount,
                    'contact_no': event.contact_no,
                    'location': event.location,
                    'basic_deliverables': event.basic_deliverables
                }
            form = form_class(initial=initial_data)
        
        return render(request, f'listings/edit_{event_type}.html', {
            'form': form,
            'event': event,
            'event_type': event_type
        })
        
    except (SponsorEvent.DoesNotExist, CollegeEvent.DoesNotExist):
        messages.error(request, 'Event not found')
        return redirect('profile')
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        return redirect('profile')