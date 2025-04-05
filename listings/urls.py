from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='listings/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/sponsor/', views.register_sponsor, name='register_sponsor'),
    path('register/college/', views.register_college, name='register_college'),
    
    # Dashboard URLs
    path('sponsor/dashboard/', views.sponsor_dashboard, name='sponsor_dashboard'),
    path('college/dashboard/', views.college_dashboard, name='college_dashboard'),
    
    # Event Creation URLs
    path('sponsor/event/create/', views.create_sponsor_event, name='create_sponsor_event'),
    path('college/event/create/', views.create_college_event, name='create_college_event'),
    
    # Request URLs
    path('event/request/<int:event_id>/', views.send_event_request, name='send_event_request'),
    path('my-requests/', views.my_requests, name='my_requests'),
    path('my-history/', views.my_history, name='my_history'),
]