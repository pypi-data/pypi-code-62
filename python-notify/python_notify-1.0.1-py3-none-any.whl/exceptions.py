import inspect
import typing
import dataclasses


class NotifyException(Exception):
    """
    Base notify lib exception.
    """


@dataclasses.dataclass(frozen=True)
class InvalidSlotSignature(NotifyException):
    """
    Signal signature does not match slot signature.
    """
    signal_signature: inspect.Signature
    slot_signature: inspect.Signature


@dataclasses.dataclass(frozen=True)
class CantConnectSameCallbackTwice(NotifyException):
    """
    Can not connect one slot to signal twice.
    """
    slot: callable


@dataclasses.dataclass(frozen=True)
class WrongSignalNotifyArgs(NotifyException):
    """
    Signal's notify was called with wrong arguments.
    """
    signal_signature: inspect.Signature
    signal_notify_called_with_args: typing.Any
