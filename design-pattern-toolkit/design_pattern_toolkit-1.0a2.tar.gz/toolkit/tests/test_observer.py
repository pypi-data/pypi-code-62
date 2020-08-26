from enum import IntFlag
from typing import Any


from toolkit.behaviour.observer import BaseEvent, BaseObserver, DefaultPublisher


class EventType(IntFlag):
    STATE_CHANGE = 2
    DOCUMENT_ADDED = 3
    DOCUMENT_DELETED = 5
    NEW_USER_REGISTERED = 7


class Observer(BaseObserver):
    def update(self, event: BaseEvent = None, source: Any = None, state=None) -> None:
        return NotImplemented


class TestEvent(BaseEvent):
    pass


def test_event():
    e = TestEvent(identity=EventType.NEW_USER_REGISTERED, name='NewUserRegistration')
    observer = Observer()
    e.attach(observer)
    assert observer in e.listeners
    assert hasattr(observer, 'update')


def test_default_publisher():
    d = DefaultPublisher()
    e = TestEvent(identity=EventType.NEW_USER_REGISTERED, name='NewUserRegistration',
                  cancelable=False)
    observer = Observer()
    e.attach(observer)
    d.register(e)
    d.publish(event=e)
    assert e.identity
    assert e.cancelable is False
    d.disable_event(event=e)
    assert e.cancelable is True
    assert e.payload.get('muted') is True
    d.enable_event(event=e)
    assert e.cancelable is False
    assert e.payload.get('muted') is False
    d.publish(event=e)  # mock method to see that observer.update() is called
    d.notify_all()

