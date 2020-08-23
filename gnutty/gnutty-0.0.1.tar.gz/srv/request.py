"""!
@author atomicfruitcake

@date 2020

HTTP Request object
"""
from base64 import b64decode
from functools import lru_cache
from srv.exceptions.b64_decode_exception import B64DecodeException
from srv.methods import METHODS


class Request:

    def __init__(
        self,
        body,
        headers,
        method,
        path,
        hostname,
        content_type="application/json",
        http_version=1.0,
    ):
        self.body = body
        self.headers = headers
        self.method = self.validate_method(method)
        self.path = path
        self.hostname = hostname
        self.content_type = content_type
        self.http_version = http_version

    @property
    def content_length(self):
        return len(self.body)

    @staticmethod
    def validate_method(method):
        assert method.upper() in METHODS
        return method.upper()

    @property
    def token(self):
        return self.headers.get("token")

    @property
    def authorization(self):
        return self.headers.get("Authorization")

    @property
    def auth_type(self):
        if self.authorization:
            auth_lower = self.authorization.lower()
            if "basic" in auth_lower:
                return "basic"

            if "oauth" in auth_lower:
                return "oauth"

            if "digest" in auth_lower:
                return "digest"

            if "bearer" in auth_lower:
                return "bearer"

    @property
    @lru_cache(maxsize=128)
    def basic_auth_creds(self):
        if self.auth_type == "basic":
            self.authorization.replace("Basic", "").split()
            split = self.authorization.strip().split(" ")
            if len(split) == 1:

                try:
                    username, password = b64decode(split[0]).decode().split(':', 1)
                    return {
                        "username": username,
                        "password": password
                    }
                except:
                    raise B64DecodeException

            elif len(split) == 2:
                if split[0].strip().lower() == 'basic':
                    try:
                        username, password = b64decode(split[1]).decode().split(':', 1)
                        return {
                            "username": username,
                            "password": password
                        }
                    except:
                        raise B64DecodeException
                else:
                    raise B64DecodeException
