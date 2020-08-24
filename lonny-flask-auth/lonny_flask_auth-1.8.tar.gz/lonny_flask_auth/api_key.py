from flask import request
from .base import Strategy

class APIKeyStrategy(Strategy):
    def get_key(self):
        return request.headers.get("x-lonny-api")

    def authenticate(self, state):
        key = self.get_key()
        if key is None:
            return
        state.attempted = True
        state.user = self.get_user(key)