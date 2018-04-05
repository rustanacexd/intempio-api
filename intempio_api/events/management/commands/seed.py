from django.core.management.base import BaseCommand

from intempio_api.events.factories import SunovionEventFactory, BiogenEventFactory, ProjectFactory


class Command(BaseCommand):
    help = 'Seed data'

    def handle(self, *args, **options):
        self.stdout.write("Start seeding data.....")

        SunovionEventFactory.create_batch(50)
        BiogenEventFactory.create_batch(50)

        self.stdout.write(self.style.SUCCESS('Successfully seeded data'))
