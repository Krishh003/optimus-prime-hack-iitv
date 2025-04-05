from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from djongo import models as djongo_models

# Common choices
EVENT_TYPES = (
    ('sponsor_event', 'Sponsor Event'),
    ('college_event', 'College Event'),
)

STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('accepted', 'Accepted'),
    ('rejected', 'Rejected'),
)

class Sponsor(models.Model):
    _id = djongo_models.ObjectIdField()
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    contact_no = models.CharField(max_length=15)
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=100, default='Not Specified')

    class Meta:
        db_table = 'sponsors'  # Specify the exact collection name

    def __str__(self):
        return self.name

class College(models.Model):
    _id = djongo_models.ObjectIdField()
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    contact_no = models.CharField(max_length=15)
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    state = models.CharField(max_length=100, default='Not Specified')
    created_at = models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'colleges'  # Specify the exact collection name

    def __str__(self):
        return self.name

class SponsorListing(models.Model):
    _id = djongo_models.ObjectIdField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=100)
    description = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    contact_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class ClientListing(models.Model):
    _id = djongo_models.ObjectIdField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    event_name = models.CharField(max_length=100)
    description = models.TextField()
    required_funding = models.DecimalField(max_digits=10, decimal_places=2)
    contact_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.event_name

class SponsorEvent(models.Model):
    _id = djongo_models.ObjectIdField()
    sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE)
    event_name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    keywords = models.TextField()
    location = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sponsor_events'

    def __str__(self):
        return self.event_name

class CollegeEvent(models.Model):
    _id = djongo_models.ObjectIdField()
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    event_name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    contact_no = models.CharField(max_length=15)
    basic_deliverables = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'college_events'

    def __str__(self):
        return self.event_name

class EventRequest(models.Model):
    _id = djongo_models.ObjectIdField()
    sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE)
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    event_id = models.IntegerField()
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    basic_deliverables = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sponsor.name} - {self.college.name} - {self.event_id}"

class SponsorHistory(models.Model):
    _id = djongo_models.ObjectIdField()
    sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE)
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    event_id = models.IntegerField()
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sponsor.name} - {self.college.name} - {self.event_id}"

class CollegeSponsorshipHistory(models.Model):
    _id = djongo_models.ObjectIdField()
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE)
    event_id = models.IntegerField()
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.college.name} - {self.sponsor.name} - {self.event_id}"