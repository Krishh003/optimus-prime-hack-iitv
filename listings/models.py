from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password

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

class Sponsor(models.Model):
    class Meta:
        db_table = 'sponsors'

    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    contact_no = models.CharField(max_length=15)
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(args, kwargs)
        self.is_college = None

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self._state.adding or self._password_changed:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

class College(models.Model):
    class Meta:
        db_table = 'colleges'

    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    contact_no = models.CharField(max_length=15)
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    state = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self._state.adding or self._password_changed:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

class SponsorEvent(models.Model):
    class Meta:
        db_table = 'sponsor_events'

    sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE)
    event_name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    keywords = models.TextField()
    location = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sponsor.name} - {self.event_name}"

class CollegeEvent(models.Model):
    class Meta:
        db_table = 'college_events'

    college = models.ForeignKey(College, on_delete=models.CASCADE)
    event_name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    contact_no = models.CharField(max_length=15)
    basic_deliverables = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.college.name} - {self.event_name}"

class EventRequest(models.Model):
    sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE)
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    event_id = models.IntegerField()
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    basic_deliverables = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sponsor.name} - {self.college.name} - {self.event_type}"

class SponsorHistory(models.Model):
    sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE)
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    event_id = models.IntegerField()
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sponsor.name} - {self.event_type} - {self.amount}"

class CollegeSponsorshipHistory(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE)
    event_id = models.IntegerField()
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.college.name} - {self.event_type} - {self.amount}"