from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from intempio_api.sunovion_events.serializers import SunovionEventSerializer


class SunovionCreateEvent(CreateAPIView):
    serializer_class = SunovionEventSerializer
    permission_classes = (AllowAny,)
