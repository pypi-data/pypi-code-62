import unittest.mock as mock

from ._property import notifiable_property


class Obj:
    def __init__(self, a):
        self._a = None

        self.a = a

    @notifiable_property
    def a(self):
        return self._a

    @a.setter
    def a(self, value):
        self._a = value * 2

    @a.deleter
    def a(self):
        del self._a


def test__set__notify_a_changed():
    """
    Changing a property value will notify {property_name}_changed signal.
    """
    slot = mock.create_autospec(lambda past_value, new_value: None)
    obj = Obj(a=1)
    assert obj.a == 2

    obj.a_changed.connect(slot)
    obj.a = 2
    assert obj.a == 4
    slot.assert_called_once_with(past_value=2, new_value=4)


def test__delitem__notify_a_removed():
    """
    Removing property will notify {property_name}_removed signal.
    """
    slot = mock.create_autospec(lambda past_value: None)
    obj = Obj(a=1)
    obj.a_removed.connect(slot)

    del obj.a

    slot.assert_called_once_with(past_value=2)
