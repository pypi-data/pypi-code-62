from toolkit.behaviour.cor import BaseHandler, Registry, Request
import uuid


class HandlerA(BaseHandler):
    pass


class HandlerB(BaseHandler):
    pass


class HandlerC(BaseHandler):
    pass


def test_handler():
    request_a = Request(identity=uuid.uuid4(), context={'request': 'Sample Test A'})
    request_b = Request(identity=uuid.uuid4(), context={'request': 'Sample Test B'})
    request_c = Request(identity=uuid.uuid4(), context={'request': 'Sample Test C'})

    a = HandlerA(request=request_a)
    b = HandlerB(request=request_b)
    c = HandlerC(request=request_c)
    a.next(b)
    b.next(c)
    c.terminal = True
    a.handle(request_c)
    assert a.registered_request == request_a.identity
    assert b.registered_request == request_b.identity
    assert c.registered_request == request_c.identity
    request_d = Request(identity=uuid.uuid4(), context={'request': 'Sample Test D'})
    Registry.register(request_d, [a, b, c])
    assert a.registered_request == request_d.identity
    assert b.registered_request == request_d.identity
