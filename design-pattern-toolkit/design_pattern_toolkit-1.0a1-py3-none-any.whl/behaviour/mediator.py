from abc import ABC, abstractmethod
from collections import namedtuple
from typing import Mapping, NewType, Sequence, Any, Callable
from types import FunctionType, MethodType

Component = NewType('Component', object)


class BaseMediator(ABC):

    @abstractmethod
    def notify(self, key: str = None, args: Sequence = None, kwargs: Mapping = None) -> Any:
        """
        Called by the participating class or object wishing to send a request.
        The request is not sent directly to the handler but to a mediator
        which then forwards to appropriate class.
        The approach used is not purely following the mediator pattern.
        While the mediator pattern
        couples two communicating classes through a meddle class,
        the approach adopted here achieves the same effect
        however, by using a registry that holds references to the communicating classes.
        Calls to notify on the mediator object looks up a registry to find corresponding
        receiver which is then invoked with needed parameters
        :param key: user friendly or unique name assigned to the caller or sender
        :param args: list of positional parameters for the receiver or receiving function
        :param kwargs: dictionary of keyword arguments and values for the receiver or
        receiving function
        :return:
        """
        pass

    @abstractmethod
    def register_component(self, sender: Component, receiver: Component, key: str = None,
                           operation: str = None, reaction: str = None,
                           context: Mapping = None) -> None:
        """
        Pair a set of component such that calls from the sending
        component are managed by the receiving component
        without each component directly communicating or knowing each other
        :param sender: the source of the request or task to be performed
        :param receiver: the object that will perform the given task
        :param key: a string representing a user friendly name or label
        :param operation: the sender function or class method of the sender. If it is None,
        the sender should be a callable
        :param reaction: the receiver function or class method of the receiver.
        If this is None, the receiver should be a callable
        :param context: a dictionary of needed parameters, information,
        metadata or condition for performing task
        :return: None
        """
        pass

    @abstractmethod
    def unregister_component(self, sender: Component, receiver: Component) -> None:
        """
        Remove a sender and receiver pair from the mediator's registry
        :param sender: the source of the request or task to be performed
        :param receiver: the object that will perform the given task
        :return: None
        """
        pass


class Mediator(BaseMediator):
    __slots__ = '_registry'

    def __init__(self) -> None:
        checked = getattr(self, '_registry', None)
        if not checked:
            self._registry = dict()

    def notify(self, key: str = None, args: Sequence = None, kwargs: Mapping = None) -> Any:
        # execute a receiver action for a given sender
        if key in self._registry:
            entry = self._registry[key]
            receiver = entry.receiver
            if isinstance(entry.args, Sequence) and isinstance(entry.kwargs, Mapping):
                if entry.args and entry.kwargs:
                    return receiver(*entry.args, **entry.kwargs)
                elif entry.args:
                    return receiver(*entry.args)
                elif entry.kwargs:
                    return receiver(**kwargs)
            else:
                return receiver()

    def register_component(self, sender: Component, receiver: Component, key: str = None,
                           operation: str = None, reaction: str = None,
                           context: Mapping = None) -> None:

        def process_function(obj, func):
            callable_ = None
            if callable(obj):
                callable_ = obj
            elif hasattr(obj, '__class__') and isinstance(func, str):
                attr = getattr(obj, func)
                if callable(attr) or isinstance(attr, (FunctionType, MethodType)):
                    callable_ = attr
            elif callable(func) or isinstance(func, (FunctionType, MethodType)):
                callable_ = func
            return callable_

        def process_name(obj):
            name = None
            if isinstance(obj, (FunctionType, MethodType)):
                name = obj.__name__
            elif hasattr(obj, '__class__'):
                name = obj.__class__.__qualname__
            return name

        try:
            _sender = process_function(sender, operation)
            _receiver = process_function(receiver, reaction)
            _source = process_name(sender)
            _target = process_name(receiver)
            _key = key
            _args = None
            _kwargs = None

            if context and isinstance(context, dict):
                a = context.get('args')
                kw = context.get('kwargs')
                if a and kw:
                    _args = [*a]
                    _kwargs = {**kw}
                    del context['args']
                    del context['kwargs']
                elif a:
                    _args = [*a]
                    del context['args']
                elif kw:
                    _kwargs = {**kw}
                    del context['kwargs']

            entry = namedtuple(
                    'Entry',
                    ('sender', 'receiver', 'source', 'target', 'args', 'kwargs', 'meta'))
            self._registry[_key] = entry(
                    sender=_sender,
                    receiver=_receiver,
                    source=_source,
                    target=_target,
                    args=_args,
                    kwargs=_kwargs,
                    meta=context
            )
        except Exception:
            raise Exception

    def unregister_component(self, sender: Callable, key: str = None,
                             receiver: Callable = None) -> None:

        if callable(sender):
            # Get all entries with the sender
            entries = [key for key, entry in self._registry.items() if
                       entry.sender == sender or entry.receiver == receiver]
            for key in entries:
                del self._registry[key]

    @property
    def registry(self):
        return self._registry
