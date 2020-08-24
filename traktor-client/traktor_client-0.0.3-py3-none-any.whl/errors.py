__all__ = [
    "TraktorError",
    "InvalidConfiguration",
]
import functools


from tea_client.errors import TeaClientError
from tea_client.handler import handler as tea_handler
from tea_console.errors import ConsoleTeaError, InvalidConfiguration


class TraktorError(TeaClientError, ConsoleTeaError):
    pass


def handler(func):
    wrapped = tea_handler(func)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return wrapped(*args, **kwargs)
        except Exception as e:
            e.__class__ = TraktorError
            raise e

    return wrapper
