from django.urls import path
from .views import (HomeView, sponsor_list, client_list,
                   PricingView, create_sponsor, create_client,
                   login, signup, logout, get_current_user, refresh_token,
                   add_event, my_requests, my_history, profile, settings,
                   register_interest, create_college_event, create_sponsor_event,
                   create_admin, admin_list, delete_admin, admin_dashboard,
                   cancel_request, request_details, accept_request)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('sponsors/', sponsor_list, name='sponsor-list'),
    path('clients/', client_list, name='client-list'),
    path('pricing/', PricingView.as_view(), name='pricing'),
    path('create-sponsor/', create_sponsor, name='create-sponsor'),
    path('create-client/', create_client, name='create-client'),
    path('login/', login, name='login'),
    path('signup/', signup, name='signup'),
    path('logout/', logout, name='logout'),
    path('api/current-user/', get_current_user, name='current-user'),
    path('api/refresh-token/', refresh_token, name='refresh-token'),
    
    # Admin management URLs
    path('admin/dashboard/', admin_dashboard, name='admin-dashboard'),
    path('admin/create/', create_admin, name='create-admin'),
    path('admin/list/', admin_list, name='admin-list'),
    path('admin/delete/<str:admin_id>/', delete_admin, name='delete-admin'),
    
    # Sponsor dashboard URLs
    path('add-event/', add_event, name='add_event'),
    path('my-requests/', my_requests, name='my_requests'),
    path('my-history/', my_history, name='my_history'),
    path('profile/', profile, name='profile'),
    path('settings/', settings, name='settings'),
    path('api/events/<str:event_id>/interest/', register_interest, name='register_interest'),
    path('api/requests/<str:request_id>/cancel/', cancel_request, name='cancel-request'),
    path('api/requests/<str:request_id>/accept/', accept_request, name='accept-request'),
    path('requests/<str:request_id>/', request_details, name='request-details'),
    path('create-college-event/', create_college_event, name='create-college-event'),
    path('create-sponsor-event/', create_sponsor_event, name='create-sponsor-event'),
]