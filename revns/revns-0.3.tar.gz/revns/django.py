from django.conf import settings
from revns import BaseNotification


class Notification(BaseNotification):
    def __init__(self, *args, **kwargs):
        kwargs['api_key'] = getattr(settings, 'CLIENT_SECRET')
        stage = getattr(settings, 'STAGE')
        if stage in ['prod', 'PROD']:
            kwargs['stage'] = 'PROD'
        elif stage in ['stg', 'STG']:
            kwargs['stage'] = 'STG'
        else:
            kwargs['stage'] = 'DEV'
        super().__init__(*args, **kwargs)


class UserNotification(Notification):
    target_type = 'user'


class GroupNotification(Notification):
    target_type = 'topic'
