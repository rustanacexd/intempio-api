import uuid

from django.contrib.postgres.fields import JSONField
from django.db import models
from model_utils import Choices
from model_utils.fields import MonitorField, StatusField
from model_utils.models import TimeStampedModel


class SunovionEvent(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    requestor_name = models.CharField(max_length=100)
    date = models.CharField(max_length=20)
    time = models.CharField(max_length=20)
    period = models.CharField(max_length=10)
    duration = models.PositiveSmallIntegerField()
    participants_count = models.PositiveSmallIntegerField()
    presenters_count = models.PositiveSmallIntegerField()
    producer_required = models.BooleanField(default=False)
    rehearsal_required = models.BooleanField(default=False)
    recording_required = models.BooleanField(default=False)
    technology_check = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    presenters = JSONField()
    STATUS = Choices('new', 'reviewed', 'accepted')
    status = StatusField(default=STATUS.new)
    reviewed_at = MonitorField(monitor='status', when=['reviewed'])
    accepted_at = MonitorField(monitor='status', when=['accepted'])

    class Meta:
        ordering = ['-modified', '-created']
