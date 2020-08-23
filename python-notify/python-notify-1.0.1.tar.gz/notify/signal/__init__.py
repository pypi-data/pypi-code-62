"""
This package implements Signal descriptor providing a way to notify signals,
connect and disconnect them, handling event using callback mechanism(called here slots).

Example:

import typing

from notify.signal import Signal


class Obj:
    event_happened = Signal(data=typing.Mapping)


def event_handler(data: typing.Mapping):
    print(f'{data=}')

obj = Obj()
obj.event_happened.connect(event_handler)
obj.event_happened.notify({'key': 'value'})  # Will print "data={'key': 'value'}"
"""

from .signal import Signal
