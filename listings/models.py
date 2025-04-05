from django.db import models
from django.contrib.auth.models import User

class Sponsor(models.Model):
    sponsor_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    contact_no = models.CharField(max_length=15)
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=100, default='Not Specified')

    class Meta:
        db_table = 'sponsors'  # Specify the exact table name

    def __str__(self):
        return self.name

class College(models.Model):
    college_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    contact_no = models.CharField(max_length=15)
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    state = models.CharField(max_length=100, default='Not Specified')
    created_at = models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'colleges'  # Specify the exact table name

    def __str__(self):
        return self.name

class SponsorListing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=100)
    description = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    contact_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

class ClientListing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    event_name = models.CharField(max_length=100)
    description = models.TextField()
    required_funding = models.DecimalField(max_digits=10, decimal_places=2)
    contact_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)