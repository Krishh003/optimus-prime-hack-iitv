from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from ...models import Sponsor, College, SponsorEvent, CollegeEvent, EventRequest, SponsorHistory, CollegeSponsorshipHistory
from decimal import Decimal
import random

class Command(BaseCommand):
    help = 'Adds sample data to the database'

    def handle(self, *args, **kwargs):
        print("Adding sample data...")
        
        # Clear existing data
        print("Clearing existing data...")
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
        sponsor_data = [
            {
                'name': 'TechCorp Inc.',
                'email': 'sponsor1@techcorp.com',
                'contact_no': '+1-555-123-4567',
                'avg_rating': 4.5,
                'password': 'password123'
            },
            {
                'name': 'Global Finance',
                'email': 'sponsor2@globalfinance.com',
                'contact_no': '+1-555-234-5678',
                'avg_rating': 4.2,
                'password': 'password123'
            },
            {
                'name': 'EcoSolutions',
                'email': 'sponsor3@ecosolutions.com',
                'contact_no': '+1-555-345-6789',
                'avg_rating': 4.8,
                'password': 'password123'
            },
            {
                'name': 'InnovateTech',
                'email': 'sponsor4@innovatetech.com',
                'contact_no': '+1-555-456-7890',
                'avg_rating': 4.0,
                'password': 'password123'
            },
            {
                'name': 'HealthCare Plus',
                'email': 'sponsor5@healthcareplus.com',
                'contact_no': '+1-555-567-8901',
                'avg_rating': 4.7,
                'password': 'password123'
            }
        ]
        
        for data in sponsor_data:
            sponsor = Sponsor.objects.create(**data)
            sponsors.append(sponsor)
            self.stdout.write(f'Created sponsor: {sponsor.name}')
        
        # Create sample colleges
        colleges = []
        college_data = [
            {
                'name': 'State University',
                'email': 'college1@stateuniv.edu',
                'contact_no': '+1-555-678-9012',
                'avg_rating': 4.3,
                'state': 'California',
                'password': 'password123'
            },
            {
                'name': 'Tech Institute',
                'email': 'college2@techinst.edu',
                'contact_no': '+1-555-789-0123',
                'avg_rating': 4.6,
                'state': 'Massachusetts',
                'password': 'password123'
            },
            {
                'name': 'Liberal Arts College',
                'email': 'college3@libarts.edu',
                'contact_no': '+1-555-890-1234',
                'avg_rating': 4.1,
                'state': 'New York',
                'password': 'password123'
            },
            {
                'name': 'Community College',
                'email': 'college4@commcollege.edu',
                'contact_no': '+1-555-901-2345',
                'avg_rating': 3.9,
                'state': 'Texas',
                'password': 'password123'
            },
            {
                'name': 'Medical University',
                'email': 'college5@meduniv.edu',
                'contact_no': '+1-555-012-3456',
                'avg_rating': 4.7,
                'state': 'Illinois',
                'password': 'password123'
            }
        ]
        
        for data in college_data:
            college = College.objects.create(**data)
            colleges.append(college)
            self.stdout.write(f'Created college: {college.name}')
        
        # Create sample sponsor events
        sponsor_events = []
        sponsor_event_data = [
            {
                'sponsor': sponsors[0],
                'event_name': 'Tech Conference 2024',
                'amount': Decimal('5000.00'),
                'keywords': 'technology, innovation, conference',
                'location': 'San Francisco, CA',
                'description': 'Annual technology conference featuring the latest innovations.'
            },
            {
                'sponsor': sponsors[1],
                'event_name': 'Finance Summit',
                'amount': Decimal('7500.00'),
                'keywords': 'finance, business, summit',
                'location': 'New York, NY',
                'description': 'Summit bringing together financial experts and industry leaders.'
            },
            {
                'sponsor': sponsors[2],
                'event_name': 'Green Energy Expo',
                'amount': Decimal('3000.00'),
                'keywords': 'environment, energy, expo',
                'location': 'Portland, OR',
                'description': 'Exhibition showcasing sustainable energy solutions.'
            },
            {
                'sponsor': sponsors[3],
                'event_name': 'Innovation Hackathon',
                'amount': Decimal('4000.00'),
                'keywords': 'hackathon, innovation, technology',
                'location': 'Boston, MA',
                'description': '48-hour hackathon focused on solving real-world problems.'
            },
            {
                'sponsor': sponsors[4],
                'event_name': 'Healthcare Symposium',
                'amount': Decimal('6000.00'),
                'keywords': 'healthcare, medical, symposium',
                'location': 'Chicago, IL',
                'description': 'Symposium on the future of healthcare technology.'
            }
        ]
        
        for data in sponsor_event_data:
            event = SponsorEvent.objects.create(**data)
            sponsor_events.append(event)
            self.stdout.write(f'Created sponsor event: {event.event_name}')
        
        # Create sample college events
        college_events = []
        college_event_data = [
            {
                'college': colleges[0],
                'event_name': 'Campus Tech Fair',
                'amount': Decimal('3000.00'),
                'description': 'Annual technology fair showcasing student projects.',
                'contact_no': '+1-555-111-2222',
                'basic_deliverables': 'Booth space, promotional materials, refreshments'
            },
            {
                'college': colleges[1],
                'event_name': 'Engineering Symposium',
                'amount': Decimal('4500.00'),
                'description': 'Symposium featuring engineering innovations and research.',
                'contact_no': '+1-555-222-3333',
                'basic_deliverables': 'Presentation space, technical equipment, lunch for attendees'
            },
            {
                'college': colleges[2],
                'event_name': 'Arts Festival',
                'amount': Decimal('2000.00'),
                'description': 'Annual arts festival showcasing student creativity.',
                'contact_no': '+1-555-333-4444',
                'basic_deliverables': 'Exhibition space, materials, refreshments'
            },
            {
                'college': colleges[3],
                'event_name': 'Community Outreach Day',
                'amount': Decimal('1500.00'),
                'description': 'Day of community service and engagement.',
                'contact_no': '+1-555-444-5555',
                'basic_deliverables': 'T-shirts, supplies, lunch for volunteers'
            },
            {
                'college': colleges[4],
                'event_name': 'Medical Research Conference',
                'amount': Decimal('5000.00'),
                'description': 'Conference presenting medical research findings.',
                'contact_no': '+1-555-555-6666',
                'basic_deliverables': 'Conference room, presentation equipment, refreshments'
            }
        ]
        
        for data in college_event_data:
            event = CollegeEvent.objects.create(**data)
            college_events.append(event)
            self.stdout.write(f'Created college event: {event.event_name}')
        
        # Create sample event requests
        event_requests = []
        for i in range(10):
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
        for i in range(5):
            sponsor = random.choice(sponsors)
            college = random.choice(colleges)
            event_type = random.choice(['sponsor_event', 'college_event'])
            event_id = random.randint(1, 5)
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
        for i in range(5):
            college = random.choice(colleges)
            sponsor = random.choice(sponsors)
            event_type = random.choice(['sponsor_event', 'college_event'])
            event_id = random.randint(1, 5)
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