from django.contrib import admin

# Register your models here.
from intempio_api.sunovion_events.models import SunovionEvent


class SunovionEventAdmin(admin.ModelAdmin):
    readonly_fields = ('reviewed_at', 'accepted_at')
    list_display = ('name', 'status', 'created', 'modified', 'reviewed_at', 'accepted_at', 'id')
    list_filter = ('status', 'created', 'reviewed_at', 'accepted_at',)
    search_fields = ['id', 'name', 'requestor_name']


admin.site.register(SunovionEvent, SunovionEventAdmin)
