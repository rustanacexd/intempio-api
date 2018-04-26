from rest_framework import serializers

from intempio_api.events.models import SunovionEvent, BiogenEvent, Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'project_id', 'project_code', 'client', 'fulfilled_by', 'sow_status',
                  'invoice_sheet', 'invite_sent_by', 'invite_type', 'run_sheet',
                  'reporting', 'notes', 'contacts', 'created', 'modified')


class SunovionEventSerializer(serializers.ModelSerializer):
    project_code = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = SunovionEvent
        fields = ('id', 'name', 'email', 'phone', 'requestor_name', 'date', 'time', 'period',
                  'duration', 'participants_count', 'presenters_count', 'producer_required',
                  'rehearsal_required', 'recording_required', 'technology_check', 'notes',
                  'presenters', 'timezone', 'status', 'project', 'project_code',
                  'reviewed_at', 'accepted_at', 'created', 'modified')

        read_only_fields = ('reviewed_at', 'accepted_at')

    def get_project_code(self, obj):
        if obj.project:
            return obj.project.project_code
        return None


class BiogenEventSerializer(serializers.ModelSerializer):
    project_code = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = BiogenEvent
        fields = ('id', 'name', 'email', 'phone', 'requestor_name', 'date', 'time', 'eod_webcast',
                  'ms_sma', 'period', 'slide_deck_name', 'slide_deck_id', 'program_meeting_id',
                  'duration', 'timezone', 'participants_count', 'presenters_count', 'notes',
                  'presenters', 'status', 'project', 'project_code', 'reviewed_at', 'accepted_at',
                  'created', 'modified')

        read_only_fields = ('reviewed_at', 'accepted_at')

    def get_project_code(self, obj):
        if obj.project:
            return obj.project.project_code
        return None
