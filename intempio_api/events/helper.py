import requests
from django.conf import settings


def send_slack_notification(event_id, event_name, channel):
    channels = {
        'sunovion': {
            'hook_url': 'https://hooks.zapier.com/hooks/catch/2825524/kvrbna/',
            'resource_prefix': 'sunovion-events'
        },
        'biogen': {
            'hook_url': 'https://hooks.zapier.com/hooks/catch/2825524/kvser5/',
            'resource_prefix': 'biogen-events'
        }
    }
    if settings.ENVIRONMENT_NAME == 'PRODUCTION':
        base_url = settings.ADMIN_URL
        url = f'{base_url}/#/{channels[channel]["resource_prefix"]}/edit-event/{event_id}'

        r = requests.post(channels[channel]['hook_url'], {
            'event_id': event_id,
            'event_name': event_name,
            'url': url
        })
        r.raise_for_status()


def submit_to_kissflow(data):
    r = requests.post(
        'https://kf-0002208.appspot.com/api/1//Event Creation/submit',
        json=data,
        headers={
            'api_key': settings.KISSFLOW_API_KEY,
            'email_id': settings.KISSFLOW_EMAIL_ID
        })
