from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from ...models import Sponsor, College, SponsorEvent, CollegeEvent, EventRequest, SponsorHistory, CollegeSponsorshipHistory
from decimal import Decimal
import random
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Adds sample data to the database'

    def handle(self, *args, **options):
        self.stdout.write('Adding sample data...')
        
        # Clear existing data
        self.stdout.write('Clearing existing data...')
        SponsorHistory.objects.all().delete()
        CollegeSponsorshipHistory.objects.all().delete()
        EventRequest.objects.all().delete()
        CollegeEvent.objects.all().delete()
        SponsorEvent.objects.all().delete()
        College.objects.all().delete()
        Sponsor.objects.all().delete()
        
        # Create a superuser if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin')
            self.stdout.write('Created superuser: admin/admin')
        
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
            self.stdout.write(f'Created sponsor: {sponsor.name}')
        
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
            self.stdout.write(f'Created college: {college.name}')
        
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
                self.stdout.write(f'Created sponsor event: {event.event_name}')
        
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
                self.stdout.write(f'Created college event: {event.event_name}')
        
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
                basic_deliverables='Logo placement, social media mentions, booth space'
            )
            event_requests.append(request)
            self.stdout.write(f'Created event request: {sponsor.name} - {college.name}')
        
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
            self.stdout.write(f'Created sponsor history: {sponsor.name} - {college.name}')
        
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
            self.stdout.write(f'Created college sponsorship history: {college.name} - {sponsor.name}')
        
        self.stdout.write(self.style.SUCCESS('Successfully added sample data')) 