from mongoengine import Document, EmbeddedDocument, fields
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

class Sponsor(Document):
    name = fields.StringField(max_length=255)
    email = fields.EmailField(unique=True)
    contact_no = fields.StringField(max_length=15)
    avg_rating = fields.DecimalField(precision=2, default=0.00)
    created_at = fields.DateTimeField()
    password = fields.StringField(max_length=255)
    address = fields.StringField(max_length=255, required=False)
    state = fields.StringField(max_length=100, default='Not Specified')

    meta = {'collection': 'sponsors'}

    def __str__(self):
        return self.name

class College(Document):
    name = fields.StringField(max_length=255)
    email = fields.EmailField(unique=True)
    contact_no = fields.StringField(max_length=15)
    avg_rating = fields.DecimalField(precision=2, default=0.00)
    state = fields.StringField(max_length=100, default='Not Specified')
    created_at = fields.DateTimeField()
    password = fields.StringField(max_length=255)
    address = fields.StringField(max_length=255, required=False)

    meta = {'collection': 'colleges'}

    def __str__(self):
        return self.name

class SponsorListing(Document):
    sponsor = fields.ReferenceField(Sponsor)
    name = fields.StringField(max_length=100)
    description = fields.StringField()
    budget = fields.DecimalField(precision=2)
    contact_email = fields.EmailField()
    created_at = fields.DateTimeField()
    is_active = fields.BooleanField(default=False)

    meta = {'collection': 'sponsor_listings'}

    def __str__(self):
        return self.name

class ClientListing(Document):
    college = fields.ReferenceField(College)
    event_name = fields.StringField(max_length=100)
    description = fields.StringField()
    required_funding = fields.DecimalField(precision=2)
    contact_email = fields.EmailField()
    created_at = fields.DateTimeField()
    is_active = fields.BooleanField(default=False)

    meta = {'collection': 'client_listings'}

    def __str__(self):
        return self.event_name

class SponsorEvent(Document):
    sponsor = fields.ReferenceField(Sponsor)
    event_name = fields.StringField(max_length=255)
    amount = fields.DecimalField(precision=2)
    keywords = fields.StringField()
    location = fields.StringField(max_length=255)
    description = fields.StringField()
    created_at = fields.DateTimeField()

    meta = {'collection': 'sponsor_events'}

    def __str__(self):
        return self.event_name

class CollegeEvent(Document):
    college = fields.ReferenceField(College)
    event_name = fields.StringField(max_length=255)
    amount = fields.DecimalField(precision=2)
    description = fields.StringField()
    contact_no = fields.StringField(max_length=15)
    basic_deliverables = fields.StringField()
    created_at = fields.DateTimeField()

    meta = {'collection': 'college_events'}

    def __str__(self):
        return self.event_name

class EventRequest(Document):
    sponsor = fields.ReferenceField(Sponsor)
    college = fields.ReferenceField(College)
    event_id = fields.IntField()
    event_type = fields.StringField(max_length=20, choices=EVENT_TYPES)
    status = fields.StringField(max_length=20, choices=STATUS_CHOICES, default='pending')
    price = fields.DecimalField(precision=2)
    basic_deliverables = fields.StringField()
    created_at = fields.DateTimeField()

    meta = {'collection': 'event_requests'}

    def __str__(self):
        return f"{self.sponsor.name} - {self.college.name} - {self.event_id}"

class SponsorHistory(Document):
    sponsor = fields.ReferenceField(Sponsor)
    college = fields.ReferenceField(College)
    event_id = fields.IntField()
    event_type = fields.StringField(max_length=20, choices=EVENT_TYPES)
    amount = fields.DecimalField(precision=2)
    created_at = fields.DateTimeField()

    meta = {'collection': 'sponsor_history'}

    def __str__(self):
        return f"{self.sponsor.name} - {self.college.name} - {self.event_id}"

class CollegeSponsorshipHistory(Document):
    college = fields.ReferenceField(College)
    sponsor = fields.ReferenceField(Sponsor)
    event_id = fields.IntField()
    event_type = fields.StringField(max_length=20, choices=EVENT_TYPES)
    amount = fields.DecimalField(precision=2)
    created_at = fields.DateTimeField()

    meta = {'collection': 'college_sponsorship_history'}

    def __str__(self):
        return f"{self.college.name} - {self.sponsor.name} - {self.event_id}"