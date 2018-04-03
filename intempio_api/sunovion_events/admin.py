from django.contrib import admin

# Register your models here.
from intempio_api.sunovion_events.models import SunovionEvent

admin.site.register(SunovionEvent)