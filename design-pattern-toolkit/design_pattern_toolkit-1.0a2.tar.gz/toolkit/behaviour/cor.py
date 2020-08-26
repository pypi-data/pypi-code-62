from abc import ABC, abstractmethod
from enum import Enum
from typing import Sequence, Mapping, Any
import uuid


class Request:
    """
    The Request class represents a task, responsibility or job to be done by respective
    handlers. A request can be identified by the _identity attribute which should be a fixed
    constant that is unique. Example, a hash, uuid, id, or enum can be used as _identity.
    The _context attribute defines any data to be passed to the handler in order to perform
    task.
    """
    __slots__ = '_identity', '_context'

    def __init__(self, identity: Any, context: Mapping = None) -> None:
        if isinstance(identity, (Enum, str, uuid.UUID, int)):
            self._identity = identity
        if isinstance(context, Mapping):
            self._context = context

    @property
    def identity(self):
        return self._identity

    @identity.setter
    def identity(self, value):
        if isinstance(value, (str, Enum, int, uuid.UUID)):
            self._identity = value

    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, value):
        if isinstance(value, Mapping):
            self._context = value
        else:
            raise ValueError('Invalid context object provided.')


class AbstractBaseHandler(ABC):

    @abstractmethod
    def handle(self, request: Request):
        pass

    @abstractmethod
    def next(self, handler):
        pass

    @abstractmethod
    def execute(self, request):
        pass

    @abstractmethod
    def register(self, request):
        pass


class Registry:

    def __init__(self):
        raise RuntimeError('This class should not be initiated')

    @classmethod
    def register(cls, request, handlers):
        if not isinstance(request, Request):
            raise RuntimeError('Invalid object provided as request. Expected type Request, '
                               'got %s' % type(request))
        if isinstance(handlers, Sequence):
            registry = [x for x in handlers if isinstance(x, BaseHandler)]
            if registry:
                for handler in registry:
                    handler.register(request)
        elif isinstance(handlers, BaseHandler):
            handlers.register(request)


class BaseHandler(AbstractBaseHandler):

    __slots__ = 'registered_request', '_handler'

    def __init__(self, request: Request, handler: Any = None) -> None:
        if isinstance(handler, BaseHandler):
            self._handler = handler
        else:
            self._handler = None
        if isinstance(request, Request):
            self.registered_request = request.identity

    def handle(self, request: Request) -> Any:
        if isinstance(request, Request):
            if request.identity == self.registered_request:
                return self.execute(request)
            else:
                return self._handler.handle(request)

    def next(self, handler: AbstractBaseHandler) -> None:
        if isinstance(handler, BaseHandler):
            self._handler = handler

    def execute(self, request: Request):
        # override in concrete implementation of handlers
        return NotImplemented

    def register(self, request: Request):
        if not isinstance(request, Request):
            raise ValueError('Invalid request object provided')
        else:
            self.registered_request = request.identity
