from hashlib import sha256

from toolkit.behaviour.mediator import Mediator

mediator = Mediator()


class ASender:
    mediator = None
    label = 'A fixed key for sender'
    key = None

    def __init__(self):
        global mediator
        self.mediator = mediator
        self.key = sha256(str.encode(self.label)).hexdigest()[:32]

    def operation(self, *args, **kwargs):
        # do stuff and pass to mediator
        self.mediator.notify(key=self.key, *args, **kwargs)
        print('Running from func: <Asender.operation>')


class BReceiver:
    mediator = None
    key = 'A fixed key for receiver'

    def react_on(self, *args, **kwargs):
        print('Running from func: <BReceiver.react_on>')


a = ASender()
b = BReceiver()


def test_registration():
    mediator.register_component(sender=a,
                                receiver=b, key=a.key,
                                operation='operation', reaction='react_on',
                                context=None)
    a.operation()
    assert a.key
    assert a.key in mediator.registry
    record = mediator.registry[a.key]
    assert callable(record.sender)
    assert callable(record.receiver)
    assert record.source == a.__class__.__qualname__
    assert record.target == b.__class__.__qualname__


def test_unregister():
    # Would invoke the registered receiver, b_sender or BReceiver.react_on
    mediator.unregister_component(sender=a.operation, key=a.key)
    assert a.key not in mediator.registry
