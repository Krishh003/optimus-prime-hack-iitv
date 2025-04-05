#!/usr/bin/env python
import os
import django
import random
from decimal import Decimal
from datetime import datetime, timedelta
from django.contrib.auth.hashers import make_password
from django.db import connection

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sponsorship_site.settings')
django.setup()

# Import models after Django setup
from listings.models import Sponsor, College, SponsorEvent, CollegeEvent, EventRequest, SponsorHistory, CollegeSponsorshipHistory

# Clear existing data
Sponsor.objects.all().delete()
College.objects.all().delete()
SponsorEvent.objects.all().delete()
CollegeEvent.objects.all().delete()
EventRequest.objects.all().delete()
SponsorHistory.objects.all().delete()
CollegeSponsorshipHistory.objects.all().delete()

# Create sample sponsors
sponsors = []
for i in range(10):
    sponsor = Sponsor.objects.create(
        name=f'Sponsor {i+1}',
        email=f'sponsor{i+1}@example.com',
        contact_no=f'9876543{i:03d}',
        avg_rating=Decimal(random.uniform(3.5, 5.0)).quantize(Decimal('0.01')),
        password=make_password('password123'),
        address=f'Address {i+1}, City {i+1}',
        state=f'State {i+1}'
    )
    sponsors.append(sponsor)
    print(f'Created sponsor: {sponsor.name}')

# Create sample colleges
colleges = []
for i in range(10):
    college = College.objects.create(
        name=f'College {i+1}',
        email=f'college{i+1}@example.com',
        contact_no=f'9876543{i+10:03d}',
        avg_rating=Decimal(random.uniform(3.5, 5.0)).quantize(Decimal('0.01')),
        state=f'State {i+1}',
        password=make_password('password123'),
        address=f'Address {i+1}, City {i+1}'
    )
    colleges.append(college)
    print(f'Created college: {college.name}')

# Create sample sponsor events
sponsor_events = []
for sponsor in sponsors:
    for i in range(3):
        event = SponsorEvent.objects.create(
            sponsor=sponsor,
            event_name=f'Sponsor Event {i+1} by {sponsor.name}',
            amount=Decimal(random.randint(10000, 50000)),
            keywords=f'keyword1, keyword2, keyword3',
            location=f'Location {i+1}',
            description=f'Description for event {i+1} by {sponsor.name}'
        )
        sponsor_events.append(event)
        print(f'Created sponsor event: {event.event_name}')

# Create sample college events
college_events = []
for college in colleges:
    for i in range(3):
        event = CollegeEvent.objects.create(
            college=college,
            event_name=f'College Event {i+1} by {college.name}',
            amount=Decimal(random.randint(50000, 200000)),
            description=f'Description for event {i+1} by {college.name}',
            contact_no=f'9876543{i+20:03d}',
            basic_deliverables='Logo placement, social media mentions, booth space'
        )
        college_events.append(event)
        print(f'Created college event: {event.event_name}')

# Create sample event requests
event_requests = []
for _ in range(20):
    sponsor = random.choice(sponsors)
    college = random.choice(colleges)
    event_type = random.choice(['sponsor_event', 'college_event'])
    
    if event_type == 'sponsor_event':
        event_id = random.choice(sponsor_events).id
    else:
        event_id = random.choice(college_events).id
        
    status = random.choice(['pending', 'accepted', 'rejected'])
    price = Decimal(random.randint(1000, 5000))
    
    request = EventRequest.objects.create(
        sponsor=sponsor,
        college=college,
        event_id=event_id,
        event_type=event_type,
        status=status,
        price=price,
        basic_deliverables="Basic deliverables for the event"
    )
    event_requests.append(request)
    print(f'Created event request: {sponsor.name} - {college.name}')

# Create sample sponsor history
for _ in range(30):
    sponsor = random.choice(sponsors)
    college = random.choice(colleges)
    event_type = random.choice(['sponsor_event', 'college_event'])
    
    if event_type == 'sponsor_event':
        event_id = random.choice(sponsor_events).id
    else:
        event_id = random.choice(college_events).id
        
    amount = Decimal(random.randint(1000, 5000))
    
    history = SponsorHistory.objects.create(
        sponsor=sponsor,
        college=college,
        event_id=event_id,
        event_type=event_type,
        amount=amount
    )
    print(f'Created sponsor history: {sponsor.name} - {college.name}')

# Create sample college sponsorship history
for _ in range(30):
    college = random.choice(colleges)
    sponsor = random.choice(sponsors)
    event_type = random.choice(['sponsor_event', 'college_event'])
    
    if event_type == 'sponsor_event':
        event_id = random.choice(sponsor_events).id
    else:
        event_id = random.choice(college_events).id
        
    amount = Decimal(random.randint(1000, 5000))
    
    history = CollegeSponsorshipHistory.objects.create(
        college=college,
        sponsor=sponsor,
        event_id=event_id,
        event_type=event_type,
        amount=amount
    )
    print(f'Created college sponsorship history: {college.name} - {sponsor.name}')

print('Sample data creation completed!')

if __name__ == '__main__':
    add_sample_data() 