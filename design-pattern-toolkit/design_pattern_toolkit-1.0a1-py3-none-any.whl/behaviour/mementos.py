# Designing and implementing the Mementos design pattern
import itertools
import json
import pickle
from abc import ABC, abstractmethod
from collections.abc import Sequence
from datetime import datetime
from enum import IntFlag
from hashlib import sha256
from typing import Any, Dict, NewType


class ScanFormat(IntFlag):
    JSON = 2
    BYTES = 3


class Scanner:

    def __init__(self):
        raise RuntimeError('Scanner cannot should not be initialized')

    @classmethod
    def scan(cls, instance: Any, fields: Sequence = None, scan_format: IntFlag = None) -> Any:
        try:
            attributes = None
            if not fields:
                attributes = dir(instance)
            elif isinstance(fields, Sequence) and len(fields):
                attributes = set(dir(instance)) & set(fields)

            class_members = {name: getattr(instance, name) for
                             name in attributes if not callable(getattr(instance, name))}
            if isinstance(scan_format, ScanFormat):
                if format == ScanFormat.JSON:
                    return json.dumps(class_members)
                elif format == ScanFormat.BYTES:
                    return pickle.dumps(class_members)
            else:
                return pickle.dumps(class_members)
        except Exception:
            raise Exception


class Mementos:
    __slots__ = '_state', '_key', '_message', '_meta', '_identifier', '_timestamp'

    def __init__(self, originator: Any, label: str = None,
                 message: str = None, meta: Dict = None,
                 fields: Sequence = None, scan_format: ScanFormat = None) -> None:
        self._timestamp = datetime.now().timestamp()
        self._key = None
        self._meta = dict()
        self._message = ''
        self._identifier = None
        self._state = None
        module = originator.__module__ if hasattr(originator, '__module__') \
            else 'NO_DEFINED_MODULE'
        if isinstance(originator, object):
            self._state = Scanner.scan(originator, fields=fields,
                                       scan_format=scan_format)
            qualified_name = "%s%s%d" % (module,
                                         originator.__class__.__qualname__, id(originator))
            self._identifier = sha256(str.encode(qualified_name)).hexdigest()[:64]
        if isinstance(label, str) and len(label) < 50 and label.isalnum():
            self._key = sha256(str.encode(label)).hexdigest()[:32]
        if isinstance(meta, dict) and len(meta):
            meta.update({
                'created_at': datetime.fromtimestamp(self._timestamp),
                'source': originator.__class__.__qualname__,
                'qualified_name': "%s.%s" % (module,
                                             originator.__class__.__qualname__)
            })
            self._meta.update(**meta)
        else:
            self._meta = {
                'created_at': datetime.fromtimestamp(self._timestamp),
                'source': originator.__class__.__qualname__,
                'qualified_name': "%s.%s" % (module,
                                             originator.__class__.__qualname__)
            }
        self._message = str(message)

    @property
    def meta(self):
        return self._meta

    @meta.setter
    def meta(self, value):
        raise RuntimeError('State data cannot be modified')

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        raise RuntimeError('State data cannot be modified')

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        raise RuntimeError('State data cannot be modified')

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        raise RuntimeError('State data cannot be modified')

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value):
        raise RuntimeError('State data cannot be modified')

    @property
    def identifier(self):
        return self._identifier

    @identifier.setter
    def identifier(self, value):
        raise RuntimeError('State data cannot be modified')


MementosType = NewType('MementosType', Mementos)


class BaseStateManager(ABC):
    # all states are saved in the StateManager. Each state is captured as a mementos

    @abstractmethod
    def get(self, mementos: MementosType = None, label: str = None) -> MementosType:
        # retrieve mementos given the label or source object
        # returned memento must match a given originator
        pass

    @property
    @abstractmethod
    def history(self):
        # return the state of a given instance of mementos
        pass

    @abstractmethod
    def stash(self, mementos: MementosType) -> None:
        # save the system state of all StateTransaction instances or given mementos
        pass


class OriginatorMixin:

    def __init__(self) -> None:
        self.state = Mementos(originator=self, label=None, message=None,
                              fields=None, scan_format=ScanFormat.BYTES)

    def commit(self, label: str = None, message: str = None, fields: Sequence = None) -> None:
        """
        Return the mementos instance or create one to capture state
        with the state save operation
        :param label: the instance of mementos to be committed
        :param message: an optional message associated
        :param fields:
        :return:
        """
        self.state = Mementos(originator=self, label=label, message=message, fields=fields,
                              scan_format=ScanFormat.BYTES)

    def restore(self, memento: Mementos = None) -> None:
        """
        Restore an object to a given state. State should be a
        valid mementos created for the given object
        :param memento: state object captured during application run or a given process
        :return:
        """
        if not isinstance(memento, Mementos):
            raise RuntimeError(
                'Invalid object provided as state. Expected Mementos but got %s' %
                type(memento))
        _state = None
        if isinstance(memento.state, bytes):
            _state = pickle.loads(memento.state)
        elif isinstance(memento.state, str):
            # attempt to parse json string into dictionary of field-value pair
            _state = json.loads(memento.state)
        if _state:
            current = dir(self)
            fields = set(current) & set(_state)
            new = {field: _state.get(field) for field in fields}
            self.__dict__.update(new)
            self.state = Mementos(self, scan_format=ScanFormat.BYTES)


class AppStateManager(BaseStateManager):
    _history = []

    @classmethod
    def get(cls, mementos: Any = None,
            label: str = None, qualified_name: str = None) -> Any:
        search = mementos or label

        if isinstance(search, Mementos):
            def search_values(record, key=search.identifier):
                if isinstance(record, Sequence) and len(record) == 2:
                    identifier, value = record
                    return identifier != key

            return itertools.filterfalse(search_values, cls._history)

        elif isinstance(search, str):
            def search_values(record, key=''):
                if isinstance(record, Sequence) and len(record) == 2:
                    _, value = record
                    hash_key = sha256(str.encode(key)).hexdigest()[:32]
                    return value.key != hash_key

            return itertools.filterfalse(search_values, cls._history)
        elif isinstance(qualified_name, str):
            def search_values(record, name=''):
                if isinstance(record, Sequence) and len(record) == 2:
                    identifier, value = record
                    hash_name = sha256(str.encode(name)).hexdigest()[:64]
                    return identifier != hash_name

            return itertools.filterfalse(search_values, cls._history)

    @classmethod
    def history(cls) -> Sequence:
        return cls._history

    @classmethod
    def stash(cls, mementos: MementosType) -> None:
        if not isinstance(mementos, Mementos):
            raise RuntimeError(
                'Invalid state object provided. Expected Mementos got %s' %
                type(mementos))
        # ensure state is not duplicated in history
        search = list(cls.get(mementos))
        if not search:
            cls._history.append((mementos.identifier, mementos))
        elif search:
            matched = [state for identifier, state in search if
                       identifier == mementos.identifier and
                       state.timestamp == mementos.timestamp]
            if not matched:
                cls._history.append((mementos.identifier, mementos))
