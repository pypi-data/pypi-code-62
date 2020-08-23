"""
This package implements @notifiable_property decorator providing
alternative to Python's @property decorator with signals for state changes.

Example:

from notify.property import notifiable_property


class Obj:
    def __init__(self, value):
        self._value = None
        self.value = value

    @notifiable_property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value * 2

    @value.deleter
    def value(self):
        del self._value


obj = Obj(value=1)
assert obj.value == 2


def on_value_changed(past_value, new_value):
    print(f'{past_value=}, {new_value=}')

obj.value_changed.connect(on_value_changed)

obj.value = 2
# Will print 'past_value=2, new_value=4'
assert obj.value == 4


def on_value_removed(past_value):
    print(f'{past_value=}')
obj.value_removed.connect(on_value_removed)

del obj.value
# Will print 'past_value=4'
"""

from ._property import notifiable_property
