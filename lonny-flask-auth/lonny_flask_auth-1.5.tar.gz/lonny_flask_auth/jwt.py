from datetime import datetime
from .cfg import Configuration
from flask import request
from jwt.exceptions import InvalidTokenError
import jwt
from .base import Strategy, get_user

class JWTStrategy(Strategy):
    def __init__(self, secret, *, cookie = Configuration.default_jwt_cookie, expiry = None):
        self._secret = secret
        self._cookie = cookie
        self._expiry = expiry

    def authenticate(self, state):
        if self._cookie not in request.cookies:
            return
        state.attempted = True
        token = request.cookies[self._cookie]
        try:
            data = jwt.decode(token, self._secret)
            state.user = self.get_user(data)
        except InvalidTokenError:
            pass

    def grant(self, request):
        data = self.get_token(get_user())
        if self._expiry is not None:
            data["exp"] = datetime.utcnow() + self._expiry
        token = jwt.encode(data, self._secret)
        request.set_cookie(self._cookie, token)