import uuid

import arrow
from django.contrib.postgres.fields import JSONField
from django.db import models
from model_utils import Choices
from model_utils.fields import MonitorField, StatusField
from model_utils.models import TimeStampedModel
from simple_history.models import HistoricalRecords

from intempio_api.events.helper import submit_to_kissflow

TO_KF_DATE_TIME_FORMAT = 'YYYY-MM-DD HH:MM'


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
    def start_time_est(self):
        return self.start_time.to('US/Eastern')

    @property
    def start_time_est_formatted(self):
        return self.start_time_est.format(TO_KF_DATE_TIME_FORMAT)

    @property
    def end_time(self):
        return self.start_time.shift(minutes=+self.duration)

    @property
    def end_time_est(self):
        return self.start_time.to('US/Eastern')

    @property
    def end_time_est_formatted(self):
        return self.end_time_est.format(TO_KF_DATE_TIME_FORMAT)

    @property
    def prod_start(self):
        return self.start_time.shift(hours=-1)

    @property
    def prod_start_est(self):
        return self.prod_start.to('US/Eastern')

    @property
    def prod_start_est_formatted(self):
        return self.prod_start_est.format(TO_KF_DATE_TIME_FORMAT)

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
    def site_address(self):
        return 'Remote' if self.producer_required else ''

    def to_kissflow(self):
        data = {
            'EventName': self.name,
            'ExpParticipants': self.participants_count,
            'ExpectedPresenters': self.presenters_count,
            'PresentersList': self.presenters_list,
            'Client_Notes': self.notes,
            # 'Hour_': str(self.start_time_est.hour),
            # 'Minutes': str(self.start_time_est.minute),
            # 'AMPM': self.period,
            'Is_this_Event_Onsite': int(self.producer_required),
            'Onsite_Event_Address': self.site_address,
            'Client_Needs_Recording': int(self.recording_required),
            'Internal_Notes': self.project.notes,
            'Internal_Company': self.project.invite_sent_by
        }

        response = submit_to_kissflow(data)
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

    def to_kissflow(self):
        data = super().to_kissflow()
        data['ClientEventCode']: self.program_meeting_id

        response = submit_to_kissflow(data)
        return data
