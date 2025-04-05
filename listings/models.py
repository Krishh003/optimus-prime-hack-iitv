from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

EVENT_TYPE_CHOICES = [
    ('technical', 'Technical'),
    ('cultural', 'Cultural'),
    ('sports', 'Sports'),
    ('other', 'Other'),
]

class Sponsor(AbstractUser):
    contact_no = models.CharField(max_length=15, blank=True, null=True)
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00, 
                                   validators=[MinValueValidator(0), MaxValueValidator(5)])
    address = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_college = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} - {self.email}"

class College(Sponsor):
    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.is_college = True
        super().save(*args, **kwargs)

class SponsorEvent(models.Model):
    sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE, related_name='sponsor_events')
    event_name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    keywords = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sponsor.username} - {self.event_name}"

class CollegeEvent(models.Model):
    college = models.ForeignKey(Sponsor, on_delete=models.CASCADE, related_name='college_events', limit_choices_to={'is_college': True})
    event_name = models.CharField(max_length=200)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES, default='other')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    contact_no = models.CharField(max_length=15, blank=True, default='')
    basic_deliverables = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.event_name} by {self.college.username}"

class EventRequest(models.Model):
    EVENT_TYPE_CHOICES = [
        ('sponsor_event', 'Sponsor Event'),
        ('college_event', 'College Event'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE, related_name='sponsor_requests', limit_choices_to={'is_college': False})
    college = models.ForeignKey(Sponsor, on_delete=models.CASCADE, related_name='college_requests', limit_choices_to={'is_college': True})
    event = models.ForeignKey(CollegeEvent, on_delete=models.CASCADE, related_name='event_requests')
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    contact_no = models.CharField(max_length=15, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    basic_deliverables = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sponsor.username} - {self.college.username} - {self.event.event_name}"

class SponsorHistory(models.Model):
    EVENT_TYPE_CHOICES = [
        ('sponsor_event', 'Sponsor Event'),
        ('college_event', 'College Event'),
    ]

    sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE, related_name='sponsor_history_as_sponsor', limit_choices_to={'is_college': False})
    college = models.ForeignKey(Sponsor, on_delete=models.CASCADE, related_name='sponsor_history_as_college', limit_choices_to={'is_college': True})
    event = models.ForeignKey(CollegeEvent, on_delete=models.CASCADE, related_name='sponsor_history')
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sponsor.username} - {self.college.username} - {self.event.event_name}"

class CollegeSponsorshipHistory(models.Model):
    EVENT_TYPE_CHOICES = [
        ('sponsor_event', 'Sponsor Event'),
        ('college_event', 'College Event'),
    ]

    college = models.ForeignKey(Sponsor, on_delete=models.CASCADE, related_name='college_sponsorship_history_as_college', limit_choices_to={'is_college': True})
    sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE, related_name='college_sponsorship_history_as_sponsor', limit_choices_to={'is_college': False})
    event = models.ForeignKey(CollegeEvent, on_delete=models.CASCADE, related_name='college_sponsorship_history')
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.college.username} - {self.sponsor.username} - {self.event.event_name}"