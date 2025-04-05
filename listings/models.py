from mongoengine import Document, EmbeddedDocument, fields
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from datetime import datetime
from django.core.exceptions import ValidationError

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
    sponsor = fields.ReferenceField(Sponsor, required=True)
    sponsor_name = fields.StringField(required=True)
    description = fields.StringField(required=True)
    amount = fields.IntField(required=True)
    expected_attendance = fields.StringField(required=True)
    deliverables = fields.StringField(required=True)
    keywords = fields.StringField(required=True)
    location = fields.StringField(required=True)
    created_at = fields.DateTimeField(default=datetime.now)

    meta = {'collection': 'sponsor_events'}

    def __str__(self):
        return self.sponsor_name

class CollegeEvent(Document):
    college = fields.ReferenceField(College, required=True)
    event_name = fields.StringField(required=True)
    amount = fields.IntField(required=True)
    description = fields.StringField(required=True)
    contact_no = fields.StringField(required=True)
    location = fields.StringField(required=True)
    basic_deliverables = fields.StringField(required=True)
    created_at = fields.DateTimeField(default=datetime.now)

    meta = {'collection': 'college_events'}

    def __str__(self):
        return self.event_name

class EventRequest(Document):
    sponsor = fields.ReferenceField(Sponsor, required=False)
    college = fields.ReferenceField(College, required=False)
    event_id = fields.StringField(required=True)
    event_type = fields.StringField(max_length=20, choices=EVENT_TYPES, required=True)
    status = fields.StringField(max_length=20, choices=STATUS_CHOICES, default='pending')
    price = fields.DecimalField(precision=2, required=True)
    basic_deliverables = fields.StringField(required=True)
    created_at = fields.DateTimeField(default=datetime.now)

    meta = {'collection': 'event_requests'}

    def clean(self):
        # Ensure either sponsor or college is set based on event_type
        if self.event_type == 'sponsor_event':
            if not self.sponsor:
                raise ValidationError('Sponsor is required for sponsor events')
            if not self.college:
                raise ValidationError('College is required for sponsor events')
        else:  # college_event
            if not self.sponsor:
                raise ValidationError('Sponsor is required for college events')
            if not self.college:
                raise ValidationError('College is required for college events')

    def __str__(self):
        sponsor_name = self.sponsor.name if self.sponsor else 'Unknown Sponsor'
        college_name = self.college.name if self.college else 'Unknown College'
        return f"{sponsor_name} - {college_name} - {self.event_id}"

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

class Admin(Document):
    username = fields.StringField(unique=True, required=True)
    email = fields.EmailField(unique=True, required=True)
    password = fields.StringField(required=True)
    created_at = fields.DateTimeField(default=datetime.now)
    created_by = fields.ReferenceField('self', required=False)

    meta = {'collection': 'admins'}

    def __str__(self):
        return self.username

class Chat(Document):
    request = fields.ReferenceField(EventRequest, required=True)
    sender = fields.GenericReferenceField(required=True)
    receiver = fields.GenericReferenceField(required=True)
    message = fields.StringField(required=True)
    created_at = fields.DateTimeField(default=datetime.now)
    is_read = fields.BooleanField(default=False)
    is_typing = fields.BooleanField(default=False)
    last_typing_update = fields.DateTimeField(default=datetime.now)

    meta = {
        'collection': 'chats',
        'indexes': [
            'request',
            'created_at'
        ]
    }

    def __str__(self):
        return f"{self.sender.name} -> {self.receiver.name}: {self.message[:50]}"