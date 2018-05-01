from rest_framework import serializers

from intempio_api.events.models import SunovionEvent, BiogenEvent, Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class SunovionEventSerializer(serializers.ModelSerializer):
    date_est = serializers.SerializerMethodField()

    class Meta:
        model = SunovionEvent
        fields = '__all__'
        read_only_fields = ('reviewed_at', 'accepted_at')

    def get_date_est(self, obj):
        return obj.start_time_est_formatted


class BiogenEventSerializer(serializers.ModelSerializer):
    date_est = serializers.SerializerMethodField()

    class Meta:
        model = BiogenEvent
        fields = '__all__'
        read_only_fields = ('reviewed_at', 'accepted_at')

    def get_date_est(self, obj):
        return obj.start_time_est_formatted


class HistoricalBiogenEventSerializer(serializers.ModelSerializer):
    history_user = serializers.StringRelatedField()
    project_code = serializers.SerializerMethodField()

    class Meta:
        model = BiogenEvent.history.model
        fields = '__all__'

    def get_project_code(self, obj):
        return obj.project.project_code if obj.project else None


class HistoricalSunovionEventSerializer(serializers.ModelSerializer):
    history_user = serializers.StringRelatedField()
    project_code = serializers.SerializerMethodField()

    class Meta:
        model = SunovionEvent.history.model
        fields = '__all__'

    def get_project_code(self, obj):
        return obj.project.project_code if obj.project else None
