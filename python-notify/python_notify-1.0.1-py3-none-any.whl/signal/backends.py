import abc
import typing
import weakref
import inspect
import itertools

from ._connection import Connection
from ..exceptions import WrongSignalNotifyArgs, InvalidSlotSignature, CantConnectSameCallbackTwice


class ISignalBackend(abc.ABC):
    def __init__(self, name, signature):
        self._name = name
        self._signature = signature

    @abc.abstractmethod
    def connect(self, slot: callable, **kwargs):
        """
        Connect slot to the signal.

        If slot signature does not match to signal's raise InvalidSlotSignature.
        If slot is already connected to this signal raise CantConnectSameCallbackTwice.

        :param slot: callback to be connected with this signal
        :param kwargs: additional kwargs (subclasses with own connect method can pass them and handle themselves)
        """
        pass

    @abc.abstractmethod
    def disconnect_all(self, **kwargs):
        """
        Disconnect all slots from the signal.

        :param kwargs: additional kwargs (subclasses with own connect method can pass them and handle themselves)
        """
        pass

    @abc.abstractmethod
    def disconnect(self, slot: callable, **kwargs):
        """
        Disconnect specific slot from the signal.

        :param slot: callback to be disconnected
        :param kwargs: additional kwargs (subclasses with own connect method can pass them and handle themselves)
        """

    @abc.abstractmethod
    def notify(self, *args, **kwargs):
        """
        Loop for slots and call them with *args, **kwargs.

        :param args: positional parameters as signal and later slots arguments
        :param kwargs: keyword parameters as signal and later slots arguments
        """

    def __str__(self):
        return f'{self._name}: {self._signature}'


class DefaultSignalBackend(ISignalBackend):
    def __init__(self, name: str, signature: inspect.Signature):
        super().__init__(name, signature)

        self._slots: typing.List[callable] = []

    def connect(self, slot: callable, **kwargs):
        """
        Connect slot to the signal.

        If slot signature does not match to signal's raise InvalidSlotSignature.
        If slot is already connected to this signal raise CantConnectSameCallbackTwice.

        If notify is in processing now (connect() called in slot connected to this signal)
        the current notification will be completed without just connected slot
        in the sense it is not be called in current notify process.

        :param slot: callback to be connected with this signal
        :param kwargs: additional kwargs (subclasses with own connect method can pass them and handle themselves)
        """
        try:
            self.__get_slot_index(slot)
        except LookupError:
            self.__validate_signature_similarity(slot=slot)

            slot = weakref.WeakMethod(slot) if inspect.ismethod(slot) else weakref.ref(slot)
            self._slots.append(slot)

            return Connection(self, slot)
        else:
            raise CantConnectSameCallbackTwice(slot)

    def disconnect_all(self, **kwargs):
        """
        Disconnect all slots from the signal.

        If notify is in processing now (disconnect_all() called in slot connected to this signal)
        the current notification will be completed in the sense that all slots will be called
        regardless of the call disconnect_all().

        :param kwargs: additional kwargs (subclasses with own connect method can pass them and handle themselves)
        """
        self._slots = []

    def disconnect(self, slot: callable, **kwargs):
        """
        Disconnect specific slot from the signal.

        If there is not such slot do nothing.

        Follows the same principle as disconnect,
        provided that the slot was disconnected during the notification process.

        :param slot: callback to be disconnected
        :param kwargs: additional kwargs (subclasses with own connect method can pass them and handle themselves)
        """
        try:
            index_to_remove = self.__get_slot_index(slot)
        except LookupError:
            pass
        else:
            self._slots.pop(index_to_remove)

    def notify(self, *args, **kwargs):
        """
        If *args, **kwargs do not match with signal signature raise WrongSignalNotifyArgs.

        If all is ok loop for current connected slots and call them with *args, **kwargs.

        :param args: positional parameters as signal and later slots arguments
        :param kwargs: keyword parameters as signal and later slots arguments
        """
        try:
            self._signature.bind(*args, **kwargs)
        except TypeError:
            raise WrongSignalNotifyArgs(signal_signature=self._signature,
                                        signal_notify_called_with_args=(args, kwargs))
        else:
            self._slots = list(self.__get_alive_slots())
            for slot in self._slots[:]:
                if slot := slot():
                    slot(*args, **kwargs)

    def __get_slot_index(self, slot: callable):
        for i, item in enumerate(self._slots):
            if item() == slot:
                return i
        raise LookupError

    def __get_alive_slots(self):
        return (slot_ref for slot_ref in self._slots if slot_ref())

    def __validate_signature_similarity(self, slot: callable):
        slot_signature = inspect.signature(slot)
        params = itertools.zip_longest(self._signature.parameters.values(), slot_signature.parameters.values())

        for signal_param, slot_param in params:
            if not all((signal_param, slot_param)):
                break
            if signal_param.name != slot_param.name or signal_param.kind != slot_param.kind:
                break
        else:
            return
        raise InvalidSlotSignature(self._signature, slot_signature)
