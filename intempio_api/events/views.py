from django_filters import rest_framework as filters
from rest_framework import mixins
from rest_framework.decorators import list_route
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from intempio_api.events.helper import send_slack_notification
from intempio_api.events.models import BiogenEvent, SunovionEvent, Project
from intempio_api.events.serializers import SunovionEventSerializer, BiogenEventSerializer, ProjectSerializer


class BiogenEventModelViewSet(ModelViewSet):
    queryset = BiogenEvent.objects.all().select_related('project')
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


class SunovionEventModelViewSet(ModelViewSet):
    queryset = SunovionEvent.objects.all().select_related('project')
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
