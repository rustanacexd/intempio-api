import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from model_utils import Choices
from rest_framework.authtoken.models import Token


class Role(models.Model):
    ROLE_CHOICES = Choices('client', 'staff', 'sunovion', 'biogen')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    ROLES = Choices('client', 'staff')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    roles = models.ManyToManyField(Role)

    def __str__(self):
        return self.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
