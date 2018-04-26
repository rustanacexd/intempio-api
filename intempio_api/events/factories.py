import json
from random import randint

import factory
from faker import Faker

from intempio_api.events.models import SunovionEvent, BiogenEvent, Project

fake = Faker()


class ProjectFactory(factory.django.DjangoModelFactory):
    project_code = factory.Sequence(lambda n: f'2018.00{n} - Dummy Project Code {n}')
    project_id = factory.Sequence(lambda n: f'2017.02{n}')
    client = factory.Iterator(Project.CLIENT, getter=lambda c: c[0])
    fulfilled_by = factory.Iterator(Project.INTERNAL_CLIENT, getter=lambda c: c[0])
    sow_status = factory.Iterator(Project.SOW_STATUS, getter=lambda c: c[0])
    invoice_sheet = factory.Sequence(lambda n: f'invoice sheet {n}')
    invite_sent_by = factory.Iterator(Project.INTERNAL_CLIENT, getter=lambda c: c[0])
    invite_type = factory.Iterator(Project.INVITE_TYPE, getter=lambda c: c[0])
    run_sheet = factory.Faker('pybool')
    reporting = factory.Faker('pybool')
    notes = factory.Faker('text')
    contacts = json.loads(json.dumps([{
        'name': fake.name(),
        'email': fake.email(),
        'contact_type': 'primary',
        'phone': fake.phone_number()
    } for i in range(randint(1, 5))]))

    class Meta:
        model = Project
        django_get_or_create = ('project_id',)


class SunovionEventFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f'dummy event name {n}')
    email = factory.Faker('company_email')
    phone = factory.Faker('phone_number')
    requestor_name = factory.Faker('name')
    date = '2018-01-01'
    time = factory.Faker('time', pattern='%H:%M')
    period = factory.Iterator(SunovionEvent.PERIOD, getter=lambda c: c[0])
    duration = 60
    participants_count = randint(1, 10)
    presenters_count = randint(1, 5)
    presenters = json.loads(json.dumps([{"name": fake.name(), "email": fake.email()} for i in range(randint(1, 5))]))
    producer_required = factory.Faker('pybool')
    rehearsal_required = factory.Faker('pybool')
    recording_required = factory.Faker('pybool')
    technology_check = factory.Faker('pybool')
    notes = factory.Faker('text')
    status = factory.Iterator(SunovionEvent.STATUS, getter=lambda c: c[0])
    project = factory.SubFactory(ProjectFactory)

    class Meta:
        model = SunovionEvent
        django_get_or_create = ('name',)


class BiogenEventFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f'dummy event name {n}')
    email = factory.Faker('company_email')
    phone = factory.Faker('phone_number')
    requestor_name = factory.Faker('name')
    date = '2018-01-01'
    time = factory.Faker('time', pattern='%H:%M')
    period = factory.Iterator(BiogenEvent.PERIOD, getter=lambda c: c[0])
    duration = factory.Iterator([60, 90, 120, 240, 480], getter=lambda c: c)
    timezone = factory.Iterator(BiogenEvent.TIMEZONE, getter=lambda c: c[0])
    participants_count = randint(1, 10)
    presenters_count = randint(1, 5)
    presenters = json.loads(json.dumps([{"name": fake.name(), "email": fake.email()} for i in range(randint(1, 5))]))
    eod_webcast = factory.Iterator(BiogenEvent.EOD_WEBCAST, getter=lambda c: c[0])
    ms_sma = factory.Iterator(BiogenEvent.MS_SMA, getter=lambda c: c[0])
    slide_deck_name = factory.Sequence(lambda n: f'slide deck name {n}')
    slide_deck_id = factory.Sequence(lambda n: f'slide deck id {n}')
    program_meeting_id = factory.Sequence(lambda n: f'program meeting id {n}')
    notes = factory.Faker('text')
    status = factory.Iterator(BiogenEvent.STATUS, getter=lambda c: c[0])
    project = factory.SubFactory(ProjectFactory)

    class Meta:
        model = BiogenEvent
        django_get_or_create = ('name',)

# class ContactFactory(factory.django.DjangoModelFactory):
#     name = factory.Sequence(lambda n: f'dummy contact name {n}')
#     contact_type = factory.Iterator(Contact.CONTACT_TYPE, getter=lambda c: c[0])
#     email = factory.Faker('company_email')
#     phone = factory.Faker('phone_number')
#
#     class Meta:
#         model = Contact
#         django_get_or_create = ('name',)
