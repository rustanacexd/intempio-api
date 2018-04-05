from django.contrib import admin
from reversion.admin import VersionAdmin

from intempio_api.events.models import SunovionEvent, BiogenEvent


class EventAdmin(VersionAdmin):
    readonly_fields = ('reviewed_at', 'accepted_at')
    list_display = ('name', 'status', 'date', 'id', 'created', 'modified')
    list_filter = ('status', 'created', 'reviewed_at', 'accepted_at',)
    search_fields = ['id', 'name', 'requestor_name']
    list_per_page = 20


admin.site.register(SunovionEvent, EventAdmin)
admin.site.register(BiogenEvent, EventAdmin)
# admin.site.register(LogEntry)
