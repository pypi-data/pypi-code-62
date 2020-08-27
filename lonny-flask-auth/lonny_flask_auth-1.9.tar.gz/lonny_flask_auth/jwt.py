from datetime import datetime
from flask import request
from jwt.exceptions import InvalidTokenError
import jwt
from .base import Strategy, get_user

class JWTStrategy(Strategy):
    def __init__(self, secret, *, expiry = None):
        self._secret = secret
        self._expiry = expiry

    def get_token(self):
        return request.cookies.get("lonny-jwt")

    def authenticate(self, state):
        token = self.get_token()
        if token is None:
            return
        state.attempted = True
        try:
            data = jwt.decode(token, self._secret)
            state.user = self.get_user(data)
        except InvalidTokenError:
            pass

    def grant(self, user = None):
        user = get_user() if user is None else user
        data = self.build_token(user)
        if self._expiry is not None:
            data["exp"] = datetime.utcnow() + self._expiry
        return jwt.encode(data, self._secret).decode("utf-8")