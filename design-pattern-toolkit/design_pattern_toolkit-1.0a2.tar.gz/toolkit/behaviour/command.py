from enum import Enum
from typing import Any, Callable, Mapping, Sequence


class Command:
    __slots__ = '_rank', '_label', '_cmd', '_group', '_args', '_kwargs'

    def __init__(self, cmd: Callable, group: Any, rank: Any, label: str = None, *args,
                 **kwargs) -> None:
        """
        :param cmd: defines the callable object which represents a command
        :param group: string identifying a command by friendly user name
        :param rank: a hashable type or int depicting the rank of a command
        where it belongs to a family or group. The rank can be used to order commands if a
        group of commands in the same family are to be prioritized and executed.
        :param label: user friendly or unique name to describe command
        :param args: list of positional parameters for the command
        :param kwargs: list of keyword parameters for the command
        """
        self._rank = None
        self._args = []
        self._kwargs = {}
        self._group = None
        self._cmd = None
        self._label = None
        if isinstance(rank, int) or isinstance(rank, Enum):
            self._rank = rank
        if isinstance(args, Sequence):
            self._args = [*args]
        if isinstance(kwargs, Mapping):
            self._kwargs = {**kwargs}
        if isinstance(label, str) and label.isalnum():
            self._label = label
        if isinstance(group, str):
            self._group = group if group.isalnum() and len(group) < 50 else None
        elif isinstance(group, Enum):
            self._group = group
        if callable(cmd):
            self._cmd = cmd

    def __call__(self, *args, **kwargs):
        if isinstance(args, Sequence):
            self._args += args
        if isinstance(kwargs, dict):
            self._kwargs.update(**kwargs)
        _args = self._args.copy()
        _kwargs = self._kwargs.copy()
        return self._cmd(*_args, **_kwargs)

    @property
    def rank(self):
        return self._rank

    @property
    def group(self):
        return self._group

    @group.setter
    def group(self, value):
        raise RuntimeError('Attribute cannot be modified')

    @property
    def cmd(self):
        return self._cmd

    @cmd.setter
    def cmd(self, value):
        self._cmd = value if callable(value) else lambda: None

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        raise RuntimeError('Attribute cannot be modified')

    @property
    def args(self):
        return self._args

    @args.setter
    def args(self, value):
        if isinstance(value, Sequence) and len(value):
            self._args.append(*value)

    @property
    def kwargs(self):
        return self._kwargs

    @kwargs.setter
    def kwargs(self, value):
        if isinstance(value, dict) and len(value):
            self._kwargs.update(**value)
