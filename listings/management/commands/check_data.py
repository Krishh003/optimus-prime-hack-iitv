from django.core.management.base import BaseCommand
from ...models import Sponsor, College, SponsorEvent, CollegeEvent, EventRequest, SponsorHistory, CollegeSponsorshipHistory

class Command(BaseCommand):
    help = 'Checks data in the database'

    def handle(self, *args, **kwargs):
        print("\nChecking Sponsors:")
        sponsors = Sponsor.objects.all()
        print(f"Number of sponsors: {sponsors.count()}")
        for sponsor in sponsors:
            print(f"- {sponsor.name} ({sponsor.email})")

        print("\nChecking Colleges:")
        colleges = College.objects.all()
        print(f"Number of colleges: {colleges.count()}")
        for college in colleges:
            print(f"- {college.name} ({college.email})")

        print("\nChecking Sponsor Events:")
        sponsor_events = SponsorEvent.objects.all()
        print(f"Number of sponsor events: {sponsor_events.count()}")
        for event in sponsor_events:
            print(f"- {event.event_name} (by {event.sponsor.name})")

        print("\nChecking College Events:")
        college_events = CollegeEvent.objects.all()
        print(f"Number of college events: {college_events.count()}")
        for event in college_events:
            print(f"- {event.event_name} (by {event.college.name})") 