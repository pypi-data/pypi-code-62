import json

from gls_api_client.utils import urljoin


class ResourcePool:
    def __init__(self, endpoint, session):
        self._endpoint = endpoint
        self._session = session

    def get_url(self):
        return self._endpoint     

class CreatableResource:
    def create_item(self, item):
        res = self._session.post(self._endpoint, data=json.dumps(item))
        return res

class GettableResource:
    def fetch_item(self, code):
        param = code
        if type(param) is list:
            param = ','.join(param)
        url = urljoin(self._endpoint, param)
        res = self._session.get(url)
        return res

class ShipmentsResource(
                    ResourcePool, 
                    CreatableResource):
    pass

class ReferencesResource(
                    ResourcePool, 
                    GettableResource):
    pass

class TrackingResource(
                    ResourcePool):
    
    @property
    def references(self):
        return ReferencesResource(
                urljoin(self._endpoint, 'references'), 
                self._session
            )

class ParcelidsResource(
                    ResourcePool, 
                    GettableResource):
    pass

class PodResource(ResourcePool):

    @property
    def parcelids(self):
        return ParcelidsResource(
            urljoin(self._endpoint, "parcelids"),
            self._session
        )
