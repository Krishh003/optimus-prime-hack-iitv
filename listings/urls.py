from django.urls import path
from .views import (HomeView, sponsor_list, client_list,
                   PricingView, create_sponsor, create_client)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('sponsors/', sponsor_list, name='sponsor-list'),
    path('clients/', client_list, name='client-list'),
    path('pricing/', PricingView.as_view(), name='pricing'),
    path('create-sponsor/', create_sponsor, name='create-sponsor'),
    path('create-client/', create_client, name='create-client'),
]