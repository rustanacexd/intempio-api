from django.contrib import admin
from django.contrib.postgres.fields import JSONField
from prettyjson import PrettyJSONWidget
from simple_history.admin import SimpleHistoryAdmin

from intempio_api.events.models import SunovionEvent, BiogenEvent, Project


class EventAdmin(SimpleHistoryAdmin):
    readonly_fields = ('reviewed_at', 'accepted_at')
    list_display = ('name', 'status', 'date', 'id', 'created', 'modified')
    list_filter = ('status', 'created', 'reviewed_at', 'accepted_at',)
    search_fields = ['id', 'name', 'requestor_name']
    list_per_page = 20
    formfield_overrides = {
        JSONField: {'widget': PrettyJSONWidget}
    }


admin.site.register(SunovionEvent, EventAdmin)
admin.site.register(BiogenEvent, EventAdmin)
admin.site.register(Project)
