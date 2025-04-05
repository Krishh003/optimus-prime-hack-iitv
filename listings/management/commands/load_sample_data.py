from django.core.management.base import BaseCommand
from listings.models import Sponsor, College, SponsorEvent, CollegeEvent
from datetime import datetime

class Command(BaseCommand):
    help = 'Loads sample data into the database'

    def handle(self, *args, **kwargs):
        # Create sample sponsors
        sponsors = [
            {
                'name': 'TechCorp Solutions',
                'email': 'contact@techcorp.com',
                'contact_no': '+1-555-0123',
                'address': '123 Tech Street, Silicon Valley',
                'state': 'California',
                'password': 'hashed_password_1',
                'created_at': datetime.now()
            },
            {
                'name': 'Global Innovations Inc',
                'email': 'info@globalinnovations.com',
                'contact_no': '+1-555-0124',
                'address': '456 Innovation Drive, Boston',
                'state': 'Massachusetts',
                'password': 'hashed_password_2',
                'created_at': datetime.now()
            },
            {
                'name': 'Future Tech Labs',
                'email': 'hello@futuretech.com',
                'contact_no': '+1-555-0125',
                'address': '789 Future Avenue, Seattle',
                'state': 'Washington',
                'password': 'hashed_password_3',
                'created_at': datetime.now()
            }
        ]

        # Create sample colleges
        colleges = [
            {
                'name': 'State University',
                'email': 'events@stateuniv.edu',
                'contact_no': '+1-555-0126',
                'address': '321 University Blvd',
                'state': 'New York',
                'password': 'hashed_password_4',
                'created_at': datetime.now()
            },
            {
                'name': 'Tech Institute',
                'email': 'campus@techinst.edu',
                'contact_no': '+1-555-0127',
                'address': '654 Campus Road',
                'state': 'Texas',
                'password': 'hashed_password_5',
                'created_at': datetime.now()
            }
        ]

        # Create sponsors in database
        created_sponsors = []
        for sponsor_data in sponsors:
            sponsor = Sponsor(**sponsor_data)
            sponsor.save()
            created_sponsors.append(sponsor)

        # Create colleges in database
        created_colleges = []
        for college_data in colleges:
            college = College(**college_data)
            college.save()
            created_colleges.append(college)

        # Create sample sponsor events
        sponsor_events = [
            {
                'sponsor': created_sponsors[0],
                'event_name': 'Tech Innovation Summit 2024',
                'amount': 50000,
                'keywords': 'Technology, Innovation, Networking',
                'description': 'Annual technology innovation summit bringing together industry leaders.',
                'created_at': datetime.now()
            },
            {
                'sponsor': created_sponsors[1],
                'event_name': 'Global Business Forum',
                'amount': 75000,
                'keywords': 'Business, Leadership, Networking',
                'description': 'International business forum for industry leaders.',
                'created_at': datetime.now()
            }
        ]

        # Create sample college events
        college_events = [
            {
                'college': created_colleges[0],
                'event_name': 'Annual Tech Fest',
                'amount': 25000,
                'description': 'Annual technology festival showcasing student innovations',
                'contact_no': '+1-555-0128',
                'basic_deliverables': 'Brand visibility, Social media promotion, Product showcase',
                'created_at': datetime.now()
            },
            {
                'college': created_colleges[1],
                'event_name': 'Engineering Expo',
                'amount': 30000,
                'description': 'Engineering project exhibition and competition',
                'contact_no': '+1-555-0129',
                'basic_deliverables': 'Brand visibility, Product demonstration, Student engagement',
                'created_at': datetime.now()
            }
        ]

        # Create sponsor events in database
        for event_data in sponsor_events:
            event = SponsorEvent(**event_data)
            event.save()

        # Create college events in database
        for event_data in college_events:
            event = CollegeEvent(**event_data)
            event.save()

        self.stdout.write(self.style.SUCCESS('Successfully loaded sample data')) 