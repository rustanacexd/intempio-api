import uuid

from django.db import models
from model_utils import Choices
from model_utils.fields import MonitorField, StatusField
from model_utils.models import TimeStampedModel


class SunovionEvent(TimeStampedModel):
    PERIOD = Choices('am', 'pm')
    STATUS = Choices('new', 'reviewed', 'accepted')

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
    producer_required = models.BooleanField(default=False)
    rehearsal_required = models.BooleanField(default=False)
    recording_required = models.BooleanField(default=False)
    technology_check = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    presenters = models.TextField(blank=True)
    status = StatusField(default=STATUS.new)
    reviewed_at = MonitorField(monitor='status', when=['reviewed'], default=None, null=True, blank=True)
    accepted_at = MonitorField(monitor='status', when=['accepted'], default=None, null=True, blank=True)

    def __str__(self):
        return f'{self.name} - {self.pk}'

    class Meta:
        ordering = ['-modified', '-created']
        verbose_name_plural = "Sunovion Events"
        verbose_name = "Sunovion Event"


class BiogenEvent(TimeStampedModel):
    PERIOD = Choices('am', 'pm')
    TIMEZONE = Choices('EST', 'EU/Basel', 'EU/Dublin', 'US/NY')
    STATUS = Choices('new', 'reviewed', 'accepted')
    EOD_WEBCAST = Choices('EOD', 'Webcast')
    MS_SMA = Choices('MS', 'MSA')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    requestor_name = models.CharField(max_length=100)
    date = models.CharField(max_length=20)
    time = models.CharField(max_length=20)
    eod_webcast = models.CharField(max_length=20, choices=EOD_WEBCAST)
    ms_sma = models.CharField(max_length=20, choices=MS_SMA)
    period = models.CharField(max_length=20, choices=PERIOD)
    slide_deck_name = models.CharField(max_length=255, blank=True)
    slide_deck_id = models.CharField(max_length=255, blank=True)
    client_event_code = models.CharField(max_length=255, blank=True)
    duration = models.PositiveSmallIntegerField()
    timezone = models.CharField(max_length=20, choices=TIMEZONE, default=TIMEZONE.EST)
    participants_count = models.PositiveSmallIntegerField(blank=True, null=True)
    presenters_count = models.PositiveSmallIntegerField(blank=True, null=True)
    notes = models.TextField(blank=True)
    presenters = models.TextField(blank=True)
    status = StatusField(default=STATUS.new)
    reviewed_at = MonitorField(monitor='status', when=['reviewed'], default=None, null=True, blank=True)
    accepted_at = MonitorField(monitor='status', when=['accepted'], default=None, null=True, blank=True)

    def __str__(self):
        return f'{self.name} - {self.pk}'

    class Meta:
        ordering = ['-modified', '-created']
        verbose_name_plural = "Biogen Events"
        verbose_name = "Biogen Event"
