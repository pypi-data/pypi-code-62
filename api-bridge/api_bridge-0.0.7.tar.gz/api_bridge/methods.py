#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2020-08-15"
__version__ = "0.0.7"

__all__ = ('Method',)

from enum import Enum, auto


class AutoName(Enum):
    def _generate_next_value_(self, start, count, last_values):
        return self


class Method(AutoName):
    """HTML methods"""

    GET = auto()
    POST = auto()

    def __str__(self): return self.value


if __name__ == '__main__': pass
