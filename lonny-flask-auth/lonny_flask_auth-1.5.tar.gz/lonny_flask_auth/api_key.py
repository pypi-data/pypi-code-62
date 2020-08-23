from flask import request
from .base import Strategy
from .cfg import Configuration

class APIKeyStrategy(Strategy):
    def __init__(self, *, api_header = Configuration.default_api_key_header):
        self._api_header = api_header
    def authenticate(self, state):
        if self._api_header not in request.headers:
            return
        state.attempted = True
        api_key = request.headers[self._api_header]
        state.user = self.get_user(api_key)