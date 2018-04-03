from random import randint

import factory

from intempio_api.sunovion_events.models import SunovionEvent


class SunovionEventFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f'dummy event name {n}')
    email = factory.Faker('company_email')
    phone = factory.Faker('phone_number')
    requestor_name = factory.Faker('name')
    date = '2018-01-01'
    time = factory.Faker('time', pattern='%H:%M')
    period = 'am'
    duration = 60
    participants_count = randint(1, 10)
    presenters_count = randint(1, 5)
    producer_required = factory.Faker('pybool')
    rehearsal_required = factory.Faker('pybool')
    recording_required = factory.Faker('pybool')
    technology_check = factory.Faker('pybool')
    notes = factory.Faker('text')
    status = factory.Iterator(SunovionEvent.STATUS, getter=lambda c: c[0])

    class Meta:
        model = SunovionEvent
        django_get_or_create = ('name',)
