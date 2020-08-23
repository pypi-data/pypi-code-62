from ..signal import Signal


def notifiable_property(getter):
    return _Property(getter=getter)


class _Property:
    def __init__(self, getter: callable):
        self._changed_signal_name: str = ''
        self._removed_signal_name: str = ''

        self._getter = getter
        self._setter = None
        self._deleter = None

    def __get__(self, instance, owner):
        if not instance:
            return self
        return self._getter(instance)

    def __set__(self, instance, value):
        if not self._setter:
            raise AttributeError("can't set attribute")

        past_value = self.__get__(instance, type(instance))
        self._setter(instance, value)
        new_value = self.__get__(instance, type(instance))

        signal = object.__getattribute__(instance, self._changed_signal_name)
        signal.notify(past_value=past_value, new_value=new_value)

    def __delete__(self, instance):
        if not self._deleter:
            raise AttributeError("can't delete attribute")

        past_value = self.__get__(instance, type(instance))
        self._deleter(instance)

        signal = object.__getattribute__(instance, self._removed_signal_name)
        signal.notify(past_value=past_value)

    def setter(self, setter):
        self._setter = setter
        return self

    def deleter(self, deleter):
        self._deleter = deleter
        return self

    def __set_name__(self, owner, name):
        self._changed_signal_name = f'{name}_changed'
        self._removed_signal_name = f'{name}_removed'

        changed = Signal(past_value=object, new_value=object)
        changed.__set_name__(owner, self._changed_signal_name)
        setattr(owner, self._changed_signal_name, changed)

        removed = Signal(past_value=object)
        removed.__set_name__(owner, self._removed_signal_name)
        setattr(owner, self._removed_signal_name, removed)

