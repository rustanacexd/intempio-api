import uuid

from django.contrib.postgres.fields import JSONField
from django.db import models
from model_utils import Choices
from model_utils.fields import MonitorField, StatusField
from model_utils.models import TimeStampedModel
import arrow


class Project(TimeStampedModel):
    CLIENT = Choices('Novartis', 'Biogen', 'Vertex', 'Sunovion', 'GE')
    INTERNAL_CLIENT = Choices('Intempio', 'RVibe')
    SOW_STATUS = Choices('Client', 'Signed')
    INVITE_TYPE = Choices('single', 'recurring')
    PROJECT_CODE = Choices(
        ('2018-001-Nov', '2018.001 Nov - Legal 2018 Support'),
        ('2018-002-Bio', '2018.002 Bio - EOD HCP and SMA PEP Programs'),
        ('2018-003-Nov', '2018.003 Nov PLS 1st'),
        ('2018-005-Ver', '2018.005 Ver - VAKO 2018'),
        ('2018-007-Nov', '2018.007 Nov - Post ENETS 2018'),
        ('2018-008-Sun', '2018.008 Sun - Training Studio Session Support'),
        ('2018-008-01-Sun', '2018.008.01 Sun - Sainz January Fast Start'),
        ('2018-008-02-Sun', '2018.008.02 Sun - January New Hire Training'),
        ('2018-008-03-Sun', '2018.008.03 Sun - The Hospital Expert'),
        ('2018-008-04', '2018.008.04 Studio Maintenance'),
        ('2018-008-05-Sun', '2018.008.05 Sun - April New Hire Phase II'),
        ('2018-009-Nov', '2018.009 Nov - Onc VA Reimagining Access Meeting'),
        ('2018-011-Nov', '2018.011 Nov - Onc IDAPS Meeting'),
        ('2018-012-Nov', '2018.012 Nov - PLS IDAPS'),
        ('2018-013-Nov', '2018.013 Nov - Onc MA IDAPS'),
        ('2018-014-Nov', '2018.014 Nov - MMS Support Plan'),
        ('2018-015-Nov', '2018.015 Nov - Onc Franchise Head Sessions'),
        ('2018-016-Bio', '2018.016 Bio - WW Medical Speaker Meetings'),
        ('2018-018-Nov', '2018.018 Nov - Onc International Broadcast'),
        ('2018-019-Bio', '2018.019 Bio - FFT Training'),
        ('2018-020-Ver', '2018.020 Ver - Multi event contract'),
        ('2018-021-Nov', '2018.021 Nov - Additional Legal Support'),
        ('2018-022-Bio', '2018.022 Bio - Marketing Sessions'),
        ('2018-023-Bio', '2018.023 Bio - MS Patient Webinars'),
        ('2018-024-Nov', '2018.024 Nov - Segmented Marketing'),
        ('2018-025-GE', '2018.025 GE - NPI August')
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project_code = models.CharField(max_length=255, choices=PROJECT_CODE, unique=True)
    client = models.CharField(max_length=100, choices=CLIENT, blank=True)
    fulfilled_by = models.CharField(max_length=100, choices=INTERNAL_CLIENT, blank=True)
    sow_status = models.CharField(max_length=100, choices=SOW_STATUS, blank=True)
    invoice_sheet = models.CharField(max_length=255, blank=True)
    invite_sent_by = models.CharField(max_length=100, choices=INTERNAL_CLIENT, blank=True)
    invite_type = models.CharField(max_length=50, choices=INVITE_TYPE, blank=True)
    run_sheet = models.BooleanField(default=False)
    reporting = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    contacts = JSONField(blank=True, null=True)

    class Meta:
        ordering = ['-modified', '-created']

    def __str__(self):
        return f'{self.project_code} - {self.pk}'


class Event(TimeStampedModel):
    PERIOD = Choices('am', 'pm')
    STATUS = Choices('new', 'reviewed', 'accepted')
    TIMEZONE = Choices('US/Central', 'US/Eastern', 'US/Mountain', 'US/Pacific')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    requestor_name = models.CharField(max_length=100)
    date = models.CharField(max_length=20)
    time = models.CharField(max_length=20)
    period = models.CharField(max_length=5, choices=PERIOD, default=PERIOD.am)
    duration = models.PositiveSmallIntegerField()
    participants_count = models.PositiveSmallIntegerField(blank=True, null=True)
    presenters_count = models.PositiveSmallIntegerField(blank=True, null=True)
    timezone = models.CharField(max_length=20, choices=TIMEZONE, default=TIMEZONE['US/Eastern'])
    notes = models.TextField(blank=True)
    presenters = JSONField(blank=True, null=True)
    status = StatusField(default=STATUS.new)
    reviewed_at = MonitorField(monitor='status', when=['reviewed'], default=None, null=True, blank=True)
    accepted_at = MonitorField(monitor='status', when=['accepted'], default=None, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        abstract = True

    @property
    def prod_hours(self):
        delta_difference = (self.end_time - self.start_time).total_seconds()
        hours_difference = delta_difference / 60 / 60
        return hours_difference

    @property
    def start_time(self):
        arrow_obj = arrow.get(f'{self.date} {self.time}', 'YYYY-MM-DD h:m', tzinfo=self.timezone)
        return arrow_obj

    @property
    def end_time(self):
        return self.start_time.shift(minutes=+self.duration)

    @property
    def presenters_list(self):
        output = ''
        for presenter in self.presenters:
            name = presenter.get('name', '')
            email = presenter.get('email', '')
            output = output + f'{name}: {email}' + '\n'

        return output

    def __str__(self):
        return f'{self.name} - {self.pk}'


class SunovionEvent(Event):
    producer_required = models.BooleanField(default=False)
    rehearsal_required = models.BooleanField(default=False)
    recording_required = models.BooleanField(default=False)
    technology_check = models.BooleanField(default=False)

    class Meta:
        ordering = ['-modified', '-created']
        verbose_name_plural = "Sunovion Events"
        verbose_name = "Sunovion Event"


class BiogenEvent(Event):
    EOD_WEBCAST = Choices('EOD', 'Webcast')
    MS_SMA = Choices('MS', 'MSA')
    eod_webcast = models.CharField(max_length=20, choices=EOD_WEBCAST)
    ms_sma = models.CharField(max_length=20, choices=MS_SMA)
    slide_deck_name = models.CharField(max_length=255, blank=True)
    slide_deck_id = models.CharField(max_length=255, blank=True)
    program_meeting_id = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-modified', '-created']
        verbose_name_plural = "Biogen Events"
        verbose_name = "Biogen Event"

    def submit_to_kissflow(self):
        data = {
            'LeadContact': self.requestor_name,
            'ContactPhone': self.phone,
            'ContactEmail': self.email,
            'EventName': self.name,
            'Duration': self.duration,
            'ExpParticipants': self.participants_count,
            'ExpPresenters': self.presenters_count,
            'DocsLink': self.slide_deck_name,
            'ClientEventCode': self.slide_deck_id,
            'PresenterList': self.presenters_list,
            'InternalNotes': self.notes,
            'StartTime': self.start_time.to('US/Eastern').datetime,
            'EndTime': self.end_time.to('US/Eastern').datetime,
            'ProdHours': self.prod_hours,
            'EventStatus': 'new'
        }

        # StartTime
        # EndTime
        # ProdStart
        # MS / SMA
        # EOD / Webcast
        # Program Meeting ID

        return data
