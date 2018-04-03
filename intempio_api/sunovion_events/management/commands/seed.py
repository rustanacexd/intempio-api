from django.core.management.base import BaseCommand

from intempio_api.sunovion_events.factories import SunovionEventFactory
from intempio_api.users.models import User


class Command(BaseCommand):
    help = 'Seed data'

    def handle(self, *args, **options):
        self.stdout.write("Start seeding data.....")

        # User.objects.create_user(username='antonio', email='antonio@go2impact.com', password='11111111a')
        User.objects.create_user()
        SunovionEventFactory.create_batch(100)

        self.stdout.write(self.style.SUCCESS('Successfully seeded data'))
