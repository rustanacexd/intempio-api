from django_filters import rest_framework as filters
from rest_framework import mixins
from rest_framework.decorators import list_route, detail_route
from rest_framework.exceptions import NotFound
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from intempio_api.events.helper import send_slack_notification
from intempio_api.events.models import BiogenEvent, SunovionEvent, Project
from intempio_api.events.serializers import (
    SunovionEventSerializer, BiogenEventSerializer, ProjectSerializer,
    HistoricalBiogenEventSerializer,
    HistoricalSunovionEventSerializer)


class BiogenEventModelViewSet(ModelViewSet):
    queryset = BiogenEvent.objects.all()
    serializer_class = BiogenEventSerializer
    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ('status', 'timezone', 'project__project_code', 'project__client',
                     'project__fulfilled_by', 'project__sow_status', 'project__invite_sent_by',
                     'project__invite_type')

    search_fields = ('id', 'name', 'email', 'phone', 'requestor_name', 'project__project_code',)
    ordering_fields = ('created', 'modified', 'reviewed_at', 'accepted_at')

    def perform_create(self, serializer):
        instance = serializer.save()
        send_slack_notification(instance.pk, instance.name, 'biogen')

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    @detail_route(filter_backends=[])
    def history(self, request, pk=None):
        history = self.get_object().history.all().select_related('history_user', 'project')
        page = self.paginate_queryset(history)

        if page is not None:
            serializer = HistoricalBiogenEventSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = HistoricalBiogenEventSerializer(history, many=True)
        return Response(serializer.data)

    @detail_route(methods=['POST'])
    def revert(self, request, pk=None):
        history_id = request.data.get('history_id')
        try:
            history = self.get_object().history.get(history_id=history_id).instance.save()
        except BiogenEvent.history.model.DoesNotExist:
            raise NotFound()

        serializer = HistoricalBiogenEventSerializer(history)
        return Response(serializer.data)

    @detail_route(methods=['GET'])
    def submit_to_kissflow(self, request, pk=None):
        data = self.get_object().submit_to_kissflow()
        return Response(data)


class SunovionEventModelViewSet(ModelViewSet):
    queryset = SunovionEvent.objects.all()
    serializer_class = SunovionEventSerializer
    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ('status', 'project__project_code', 'project__client',
                     'project__fulfilled_by', 'project__sow_status', 'project__invite_sent_by',
                     'project__invite_type')

    search_fields = ('id', 'name', 'email', 'phone', 'requestor_name', 'project__project_code')
    ordering_fields = ('created', 'modified', 'reviewed_at', 'accepted_at')

    def perform_create(self, serializer):
        instance = serializer.save()
        send_slack_notification(instance.pk, instance.name, 'sunovion')

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    @detail_route(filter_backends=[])
    def history(self, request, pk=None):
        history = self.get_object().history.all().select_related('history_user', 'project')
        page = self.paginate_queryset(history)

        if page is not None:
            serializer = HistoricalSunovionEventSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = HistoricalSunovionEventSerializer(history, many=True)
        return Response(serializer.data)

    @detail_route(methods=['POST'])
    def revert(self, request, pk=None):
        history_id = request.data.get('history_id')

        try:
            history = self.get_object().history.get(history_id=history_id).instance.save()
        except SunovionEvent.history.model.DoesNotExist:
            raise NotFound()

        serializer = HistoricalSunovionEventSerializer(history)
        return Response(serializer.data)


class ProjectModelViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ('project_id', 'project_code')
    search_fields = ('id', 'project_id', 'project_code')
    ordering_fields = ('created', 'modified')

    @list_route()
    def project_codes(self, request):
        client_name = request.query_params.get('client')
        project_codes = Project.objects.filter(client=client_name).values_list('project_code', flat=True)
        return Response(project_codes)


class FindByProjectId(mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'project_code'
    # lookup_value_regex = '[\w.@+-]+'
    lookup_value_regex = '(.+)'


class UpTimeView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        return Response('Ok')
