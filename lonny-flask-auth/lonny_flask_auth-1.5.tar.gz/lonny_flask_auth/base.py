from functools import wraps
from flask import redirect, g
from .error import AuthenticationError

AUTH_STATE_KEY = "_lonny_flask_auth"

class AuthState:
    def __init__(self):
        self.attempted = False
        self.user = None

def get_auth_state():
    return g.setdefault(AUTH_STATE_KEY, AuthState())

def get_user():
    return get_auth_state().user

class Middleware:
    def __call__(self, fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):
            next_fn = lambda: fn(*args, **kwargs)
            return self.run(next_fn)
        return wrapped

class Strategy(Middleware):
    def run(self, next_fn):
        state = get_auth_state()
        if not state.attempted:
            response = self.authenticate(state)
            if response is not None:
                return response
        return next_fn()

class Guard(Middleware):
    def run(self, next_fn):
        if get_auth_state().user is None:
            raise AuthenticationError()
        return next_fn()