from flask import request
from .base import Strategy, get_user
import bcrypt

class PasswordStrategy(Strategy):
    def get_credentials_str(self):
        return request.headers.get("x-lonny-password")

    def get_credentials(self):
        header = self.get_credentials_str()
        if header is None:
            return None
        split = header.split(":")
        if len(split) != 2:
            return None
        return split

    def get_hash(self, user):
        return user["password"].tobytes()

    def authenticate(self, state):
        pair = self.get_credentials()
        if pair is None:
            return
        state.attempted = True
        email, password = pair
        user = self.get_user(email)
        if user is None or not bcrypt.checkpw(password.encode("utf-8"), self.get_hash(user)):
            return
        state.user = user