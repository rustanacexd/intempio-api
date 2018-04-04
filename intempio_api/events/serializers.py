from rest_framework import serializers

from intempio_api.events.models import SunovionEvent, BiogenEvent


class SunovionEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = SunovionEvent
        fields = '__all__'


class BiogenEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = BiogenEvent
        fields = '__all__'
