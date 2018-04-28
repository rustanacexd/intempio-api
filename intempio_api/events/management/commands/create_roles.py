from django.core.management.base import BaseCommand

from intempio_api.users.models import Role


class Command(BaseCommand):
    help = 'Seed data'

    def handle(self, *args, **options):
        self.stdout.write("creating roles data.....")

        Role.objects.create(name='client')
        Role.objects.create(name='staff')
        Role.objects.create(name='biogen')
        Role.objects.create(name='sunovion')

        self.stdout.write(self.style.SUCCESS('Successfully created roles data'))
