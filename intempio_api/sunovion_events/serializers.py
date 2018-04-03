from rest_framework import serializers

from intempio_api.sunovion_events.models import SunovionEvent


class SunovionEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = SunovionEvent
        fields = '__all__'
