import requests

DEV = 'DEV'
STG = 'STG'
PROD = 'PROD'
HOST = 'https://notification.revtel-api.com/v2'
STG_HOST = 'https://notification-stg.revtel-api.com/v2'
DEV_HOST = 'https://notification-dev.revtel-api.com/v2'


class BaseNotification:
    target_type = 'topic'

    def __init__(self, api_key, instance=None, stage='DEV'):
        if stage not in ['PROD', 'STG', 'DEV']:
            raise
        self.instance = instance
        self.api_key = api_key
        self.stage = stage

    def _get_host(self):
        if self.stage == PROD:
            return HOST
        elif self.stage == STG:
            return STG_HOST
        else:
            return DEV_HOST

    def _build_headers(self):
        return {
            'Content-Type': 'application/json',
            'x-api-key': self.api_key
        }

    def _post(self, path, data):
        url = f'{self._get_host()}{path}'
        resp = requests.post(url, headers=self._build_headers(), json=data)
        return resp

    def build_title(self):
        raise NotImplementedError

    def build_body(self):
        raise NotImplementedError

    def build_target(self):
        raise NotImplementedError

    def build_data(self):
        raise NotImplementedError

    def publish(self):
        target = self.build_target()
        path = f'/{self.target_type}/{target}'
        body = {
            'subject': self.build_title(),
            'title': self.build_title(),
            'body': self.build_body(),
            'data': self.build_data()
        }
        try:
            resp = self._post(path=path, data=body)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            return None


class UserNotification(BaseNotification):
    target_type = 'user'


class GroupNotification(BaseNotification):
    target_type = 'topic'
