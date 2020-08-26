from abc import ABC, abstractmethod
from datetime import datetime
from enum import IntFlag, Enum
from functools import wraps
from typing import Dict, Any, NewType, Sequence, Mapping
from uuid import UUID


__all__ = ('BaseEvent', 'BasePublisher', 'DefaultPublisher', 'BaseObserver', 'observe',
           'EventType')


class BaseEvent:
    """
    Models an event class for sending signal across application.
    Each signal is identified via constant name or value identified as enum
    """
    __slots__ = '_name', '_cancelable', '_source', '_timestamp', \
                '_payload', '_identity', '_listeners'

    def __init__(self, identity: Enum = None, name: str = None,
                 cancelable: bool = False, source: Any = None,
                 payload: Dict = None) -> None:
        self._listeners = set()

        self._name = name if isinstance(name, str) and len(name) < 50 and name.isalnum() \
            else None
        self._cancelable = bool(cancelable)
        self._source = source if isinstance(source, BasePublisher) else self.__class__
        self._payload = dict(payload) if isinstance(payload, Mapping) else {}
        self._timestamp = datetime.now().timestamp()
        if isinstance(identity, (Enum, int, str, UUID)):
            self._identity = identity
        else:
            raise RuntimeError(
                'Event object should have unique identity of type (Enum, int, str, UUID)')

    def notify(self) -> None:
        for listener in self._listeners:
            listener.update(event=self)

    def attach(self, listener) -> None:
        if not isinstance(listener, BaseObserver):
            raise RuntimeError('Invalid event listener object provided. '
                               'Expected Observer but got %s' % type(listener))
        if listener not in self._listeners:
            self._listeners.add(listener)

    @property
    def name(self):
        return self._name

    @property
    def cancelable(self):
        return self._cancelable

    @cancelable.setter
    def cancelable(self, value):
        self._cancelable = bool(value)

    @property
    def source(self):
        return self._source

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def payload(self):
        return self._payload

    @property
    def identity(self):
        return self._identity

    @property
    def listeners(self):
        return self._listeners


class BasePublisher(ABC):
    """
    Defines an object which can publish a set of events that
    can be consumed by other objects
    """

    @classmethod
    @abstractmethod
    def publish(cls, event: BaseEvent = None) -> None:
        """
        Publish the registered event upon satisfaction of
        listed condition (calls BaseEvent.notify())
        """
        pass

    @classmethod
    @abstractmethod
    def register(cls, event: BaseEvent, conditions: Any = None) -> None:
        """
        Add an event to the list of possible events
        which can be published by this object
        """
        pass

    @abstractmethod
    def disable_event(self, event: BaseEvent) -> None:
        """
        Disable an event when set condition are reached.
        Muted events are only implemented for given object
        and not across all instances of the class.
        Attempts to set BaseEvent.cancelable to True
        """
        pass

    @abstractmethod
    def enable_event(self, event: BaseEvent) -> None:
        """
        Enable an event when set condition are reached.
        Muted events are only implemented for given object
        and not across all instances of the class.
        """
        pass


# Sample application implementation
class EventFlag(IntFlag):
    STATE_CHANGE = 2
    DOCUMENT_ADDED = 3
    DOCUMENT_DELETED = 5
    NEW_USER_REGISTERED = 7
    BUS = 1


EventType = NewType('EventType', BaseEvent)


class BaseObserver(ABC):

    @abstractmethod
    def update(self, event: EventType = None, source: Any = None, state=None) -> None:
        pass


@wraps
def observe(event: BaseEvent, source: Any = None):
    # function/method wrapper for function to handle event by source object
    # registers the wrapped function into BusinessDocumentWatcher
    return NotImplemented


class DefaultPublisher(BasePublisher):
    _registry = dict()

    @classmethod
    def notify_all(cls):
        for conditions, signal in cls._registry.values():
            if isinstance(signal, BaseEvent) and conditions:
                if not signal.payload.get('muted'):
                    signal.notify()

    @classmethod
    def publish(cls, event: Any = None) -> None:
        """
        Publish the given event(s) upon
        satisfaction of listed condition (calls BaseEvent.notify())
        """
        if isinstance(event, BaseEvent):
            if not event.payload.get('muted'):
                event.notify()
        elif isinstance(event, Sequence):
            signals = set([signal for signal in event if isinstance(signal, BaseEvent)])
            for signal in signals:
                if not signal.payload.get('muted'):
                    signal.notify()

    @classmethod
    def register(cls, event: BaseEvent, conditions: Any = None):
        """
        Add an event to the list of possible events which
        can be published by this object
        """
        if not isinstance(event, BaseEvent):
            raise RuntimeError('Invalid object provided. '
                               'Expected Event but got %s' % type(event))
        if isinstance(conditions, bool):
            cls._registry[event.identity] = (conditions, event)

    def disable_event(self, event: BaseEvent):
        """
        Disable an event when set condition are reached.
        Muted events are only implemented for given object
        and not across all instances of the class.
        Attempts to set BaseEvent.cancelable to True
        """
        event.cancelable = True
        event.payload.update({'muted': True})
        self._registry[event.identity] = (False, event)

    def enable_event(self, event):
        """
        Enable an event when set condition are reached.
        Muted events are only implemented for given object
        and not across all instances of the class.
        """
        event.cancelable = False
        event.payload.update({'muted': False})
        self._registry[event.identity] = (True, event)
