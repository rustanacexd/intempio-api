import requests
from django.conf import settings


def send_slack_notification(event_id, event_name, channel):
    channels = {
        'sunovion': {
            'hook_url': 'https://hooks.zapier.com/hooks/catch/2825524/kvrbna/',
            'resource_prefix': 'biogen-events'
        },
        'biogen': {
            'hook_url': 'https://hooks.zapier.com/hooks/catch/2825524/kvser5/',
            'resource_prefix': 'sunovion-events'
        }
    }
    if settings.SEND_SLACK:
        base_url = settings.ADMIN_URL
        url = f'{base_url}/{channels[channel]["resource_prefix"]}/edit-event/{event_id}'

        r = requests.post(channels[channel]['hook_url'], {
            'event_id': event_id,
            'event_name': event_name,
            'url': url
        })
        r.raise_for_status()
