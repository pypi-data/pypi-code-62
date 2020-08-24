__all__ = [
    "TraktorError",
    "InvalidConfiguration",
    "HttpClientError",
    "NotFound",
    "HttpClientTimeout",
    "HttpRateLimitExceeded",
    "SerializationError",
]

import functools
from typing import Optional

from httpx import Response
from tea_console.errors import ConsoleTeaError, InvalidConfiguration
from pydantic import ValidationError as PydanticValidationError


class TraktorError(ConsoleTeaError):
    pass


class ValidationError(TraktorError):
    def __init__(self, error: PydanticValidationError):
        self.error = error
        super().__init__(message="Request Validation Error.")

    @property
    def errors(self):
        return self.error.errors()


class HttpClientError(TraktorError):
    def __init__(self, message, response=None):
        super().__init__(message)
        self.response: Response = response
        self.status_code = (
            response.status_code if response is not None else 500
        )

    @property
    def data(self):
        return self.response.json()

    def __str__(self):
        return (
            f"{self.name}(message={self.message}, "
            f"status_code={self.status_code})"
        )

    __repr__ = __str__


class NotFound(HttpClientError):
    def __init__(self, response: Optional[Response] = None):
        super().__init__(message="Object not found", response=response)


class HttpClientTimeout(HttpClientError):
    """Http timeout error."""

    def __init__(self):
        super().__init__("Timeout exceeded")


class HttpRateLimitExceeded(HttpClientError):
    def __init__(self, response, limit, remaining, reset, retry):
        super().__init__("Rate limit exceeded.", response=response)
        self.limit = limit
        self.remaining = remaining
        self.reset = reset
        self.retry = retry

    def __str__(self):
        return (
            f"{self.name}(limit={self.limit}, remaining={self.remaining}, "
            f"reset={self.reset}s, retry={self.retry}s)"
        )

    __repr__ = __str__


class SerializationError(TraktorError):
    def __init__(self, errors):
        """Thrown when the client cannot serialize or deserialize an object.

        Args:
            errors (dict): Dictionary of found errors
        """
        super().__init__("Serialization error.")
        self.errors = errors


def handler(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except PydanticValidationError as e:
            raise ValidationError(error=e)

    return wrapper
