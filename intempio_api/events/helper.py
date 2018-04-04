import requests
from django.conf import settings


def send_slack_notification(event_id, event_name, channel):
    channels = {
        'sunovion': 'https://hooks.zapier.com/hooks/catch/2825524/kvrbna/',
        'biogen': 'https://hooks.zapier.com/hooks/catch/2825524/kvser5/'
    }
    if settings.SEND_SLACK:
        base_url = settings.ROOT_URL
        url = f'{base_url}/admin/events/{channel}event/{event_id}/change/'
        r = requests.post(channels[channel], {
            'event_id': event_id,
            'event_name': event_name,
            'url': url
        })
        r.raise_for_status()
