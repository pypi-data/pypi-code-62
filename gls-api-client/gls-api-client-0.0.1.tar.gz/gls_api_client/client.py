import base64

import requests as rq

from gls_api_client import (
    resources,
    utils
)

class Client:
    BASE_URL = "https://api.gls-group.eu/public/v1"
    SANDBOX_URL = "https://api-qs.gls-group.eu/public/v1"

    def __init__(self, shipper_id, username, password, language='fr', sandbox=False):
        if language not in ['en', 'fr', 'dk', 'de']:
            raise ValueError("Invalid Language")

        self._shipper_id = shipper_id
        self._username = username
        self._language = language
        self._sandbox = sandbox
        
        self._session = rq.Session()
        self._authenticate(username, password)

        base_url = self.BASE_URL if not self._sandbox else self.SANDBOX_URL
        self._resources = {
            "shipments": resources.ShipmentsResource(
                utils.urljoin(base_url, "shipments"), self._session
            ),
            "pod": resources.PodResource(
                utils.urljoin(base_url, "pod"), self._session
            ),
            "tracking": resources.TrackingResource(
                utils.urljoin(base_url, "tracking"), self._session
            ),
        }

    def _authenticate(self, username, password):
        auth = base64.b64encode('{}:{}'.format(username, password).encode()).decode()
        headers = {
            "Accept-Language": self._language,
            "Accept": "application/json",
            "Accept-Encoding": "gzip,deflate",
            "Content-Type": "application/json",
            "Authorization": "Basic {}".format(auth)
        }
        self._session.headers = headers

    @property
    def resources(self):
        return self._resources

    @property
    def shipments(self):
        return self._resources['shipments']

    @property
    def pod(self):
        return self._resources['pod']

    @property
    def tracking(self):
        return self._resources['tracking']