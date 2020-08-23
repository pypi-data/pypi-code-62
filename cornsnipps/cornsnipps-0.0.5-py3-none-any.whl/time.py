import time
from typing import Union

__all__ = ['time_ms', 'time_us', 'time_spent_from']


def time_ms(as_float: bool = False) -> Union[int, float]:
    """Convert current time to milliseconds.

    :param as_float: result should be float, default result is int
    :return: current time in milliseconds
    """
    _time_ms = time.time() * 1000
    if not as_float:
        return int(_time_ms)
    return _time_ms


def time_us(as_float: bool = False) -> Union[int, float]:
    """Convert current time to microseconds.

    Base on the time.time() instead the time.time_ns() for backward
    compatibility.

    :param as_float: result should be float, default result is int
    :return: current time in microseconds
    """
    _time_us = time.time() * 1000000
    if not as_float:
        return int(_time_us)
    return _time_us


def time_spent_from(start_time: float) -> float:
    """Calculate time spent from start_time to now

    Example:
    >>> start_time = time.time()
    >>> ...
    >>> time_spent = time_spent_from(start_time)

    :param start_time: time in seconds since the epoch
    :return: time spent from start_time to now
    """
    return time.time() - start_time
