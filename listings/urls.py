from django.urls import path
from .views import (HomeView, sponsor_list, client_list,
                   PricingView, create_sponsor, create_client,
                   login, signup, logout, get_current_user, refresh_token)

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
    path('api/current-user/', get_current_user, name='get_current_user'),
    path('api/refresh-token/', refresh_token, name='refresh_token'),
]