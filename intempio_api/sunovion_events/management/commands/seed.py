from django.core.management.base import BaseCommand

from intempio_api.sunovion_events.factories import SunovionEventFactory


class Command(BaseCommand):
    help = 'Seed data'

    def handle(self, *args, **options):
        self.stdout.write("Start seeding data.....")

        SunovionEventFactory.create_batch(100)

        self.stdout.write(self.style.SUCCESS('Successfully seeded data'))
