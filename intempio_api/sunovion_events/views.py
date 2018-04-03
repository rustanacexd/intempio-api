from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from intempio_api.sunovion_events.serializers import SunovionEventSerializer


class SunovionCreateEvent(CreateAPIView):
    serializer_class = SunovionEventSerializer
    permission_classes = (AllowAny,)


class UpTimeView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        return Response('Ok')
