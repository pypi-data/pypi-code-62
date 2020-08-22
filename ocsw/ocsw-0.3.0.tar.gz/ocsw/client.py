from .api.client import APIClient
from .models.companies import CompanyCollection


class OctaveClient:
    def __init__(self, api_client=None, *args, **kwargs):
        self.api = api_client or APIClient(*args, **kwargs)

    @property
    def companies(self):
        return CompanyCollection(client=self)
