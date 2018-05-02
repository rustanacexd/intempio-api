import uuid

import arrow
from django.contrib.postgres.fields import JSONField
from django.db import models
from model_utils import Choices
from model_utils.fields import MonitorField, StatusField
from model_utils.models import TimeStampedModel
from simple_history.models import HistoricalRecords


class StatusMixin(object):
    STATUS = Choices('new', 'reviewed', 'accepted', 'canceled')


class Project(TimeStampedModel):
    CLIENT = Choices('Novartis', 'Biogen', 'Vertex', 'Sunovion', 'GE')
    INTERNAL_CLIENT = Choices('Intempio', 'RVibe')
    SOW_STATUS = Choices('Client', 'Signed')
    INVITE_TYPE = Choices('single', 'recurring')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project_id = models.CharField(max_length=255)
    project_code = models.CharField(max_length=255)
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


class Event(StatusMixin, TimeStampedModel):
    PERIOD = Choices('am', 'pm')
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
    status = StatusField(default=StatusMixin.STATUS.new, choices_name='STATUS')
    producer_required = models.BooleanField(default=False)
    rehearsal_required = models.BooleanField(default=False)
    recording_required = models.BooleanField(default=False)
    technology_check = models.BooleanField(default=False)
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
        arrow_obj = arrow.get(f'{self.date} {self.time}', 'YYYY-MM-DD hh:mm', tzinfo=self.timezone)
        return arrow_obj

    @property
    def start_time_est_formatted(self):
        return self.start_time.to('US/Eastern').format('YYYY-MM-DD hh:mm')

    @property
    def end_time(self):
        return self.start_time.shift(minutes=+self.duration)

    @property
    def presenters_list(self):
        output = ''
        if not self.presenters:
            return output

        for presenter in self.presenters:
            name = presenter.get('name', '')
            email = presenter.get('email', '')
            output = output + f'{name}: {email}' + '\n'

        return output

    @property
    def prod_start(self):
        return self.start_time.shift(hours=-1).datetime

    @property
    def site_address(self):
        return 'Remote' if self.producer_required else ''

    def submit_to_kissflow(self):
        data = {
            'LeadContact': self.requestor_name,
            'ContactPhone': self.phone,
            'ContactEmail': self.email,
            'EventName': self.name,
            'Duration': self.duration,
            'ExpParticipants': self.participants_count,
            'ExpPresenters': self.presenters_count,
            'PresenterList': self.presenters_list,
            'ClientNotes': self.notes,
            'StartTime': self.start_time.to('US/Eastern').datetime,
            'EndTime': self.end_time.to('US/Eastern').datetime,
            'ProdHours': self.prod_hours,
            'EventStatus': 'new',
            'ProdStart': self.prod_start,
            'ProjectCode': self.project.project_code,
            'Client': self.project.client,
            'Onsite': self.producer_required,
            'SiteAddress': self.site_address,  # TODO ALLOW NEW ADDRESS, ASK PARKER PRECAUTION OF ADDRESS
            'RecordReqs': self.recording_required,
            'DocsLink': '',
            'ClientEventCode': '',
            'rehearsal_required': self.rehearsal_required,
            'recording_required': self.recording_required,
            'technology_check': self.technology_check,
        }

        # ProducersReq # TODO
        return data

    def __str__(self):
        return f'{self.name} - {self.pk}'


class SunovionEvent(Event):
    history = HistoricalRecords(bases=[StatusMixin, models.Model])

    class Meta:
        ordering = ['-modified', '-created']
        verbose_name_plural = "Sunovion Events"
        verbose_name = "Sunovion Event"

    @property
    def prod_start(self):
        if self.producer_required:
            return self.start_time.shift(hours=-2)
        return self.start_time.shift(hours=-1)


class BiogenEvent(Event):
    EOD_WEBCAST = Choices('EOD', 'Webcast')
    MS_SMA = Choices('MS', 'MSA')
    eod_webcast = models.CharField(max_length=20, choices=EOD_WEBCAST, blank=True)
    ms_sma = models.CharField(max_length=20, choices=MS_SMA, blank=True)
    slide_deck_name = models.CharField(max_length=255, blank=True)
    slide_deck_id = models.CharField(max_length=255, blank=True)
    program_meeting_id = models.CharField(max_length=255, blank=True)
    history = HistoricalRecords(bases=[StatusMixin, models.Model])

    class Meta:
        ordering = ['-modified', '-created']
        verbose_name_plural = "Biogen Events"
        verbose_name = "Biogen Event"

    def submit_to_kissflow(self):
        data = super(BiogenEvent, self).submit_to_kissflow()
        data['DocsLink'] = self.slide_deck_name
        data['ClientEventCode'] = self.slide_deck_id

        # MS / SMA
        # EOD / Webcast

        return data
