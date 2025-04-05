from django.shortcuts import render, redirect
from .models import SponsorListing, ClientListing, Sponsor, College
from .forms import SponsorForm, ClientForm, LoginForm, SignupForm
from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
import json

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
                        refresh['user_id'] = user.sponsor_id
                        refresh['user_type'] = 'sponsor'
                        refresh['email'] = user.email
                        
                        # Store user info in session
                        request.session['user_id'] = user.sponsor_id
                        request.session['user_type'] = 'sponsor'
                        request.session['user_name'] = user.name
                        request.session['user_email'] = user.email
                        
                        # Store tokens in session
                        request.session['access_token'] = str(refresh.access_token)
                        request.session['refresh_token'] = str(refresh)
                        
                        messages.success(request, 'Successfully logged in as sponsor!')
                        return redirect('sponsor-list')
                except Sponsor.DoesNotExist:
                    pass
            else:
                try:
                    user = College.objects.get(email=email)
                    if check_password(password, user.password):
                        # Create JWT tokens with custom claims
                        refresh = RefreshToken()
                        refresh['user_id'] = user.college_id
                        refresh['user_type'] = 'college'
                        refresh['email'] = user.email
                        
                        # Store user info in session
                        request.session['user_id'] = user.college_id
                        request.session['user_type'] = 'college'
                        request.session['user_name'] = user.name
                        request.session['user_email'] = user.email
                        
                        # Store tokens in session
                        request.session['access_token'] = str(refresh.access_token)
                        request.session['refresh_token'] = str(refresh)
                        
                        messages.success(request, 'Successfully logged in as college!')
                        return redirect('client-list')
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
                    user = Sponsor.objects.create(
                        name=form.cleaned_data['name'],
                        email=form.cleaned_data['email'],
                        contact_no=form.cleaned_data['contact_no'],
                        address=form.cleaned_data['address'],
                        state=form.cleaned_data['state'],
                        password=password
                    )
                else:
                    user = College.objects.create(
                        name=form.cleaned_data['name'],
                        email=form.cleaned_data['email'],
                        contact_no=form.cleaned_data['contact_no'],
                        address=form.cleaned_data['address'],
                        state=form.cleaned_data['state'],
                        password=password
                    )
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
    
    # Add a success message
    messages.success(request, 'You have been successfully logged out.')
    
    # Redirect to login page
    return redirect('login')

# API endpoint to get current user info
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

# API endpoint to refresh token
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