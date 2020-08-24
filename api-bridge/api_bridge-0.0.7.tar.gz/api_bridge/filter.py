#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2020-08-15"
__version__ = "0.0.5"

__all__ = ('Filter',)

from operator import getitem
from api_bridge.exceptions import APIException

from typing import Dict, Any


class Filter:
    out: Dict[str, Any]

    def __init__(self, **out: str):
        self.out = out

    def __call__(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if self.out is None: return dict()
        output = dict()
        try:
            for name, value, in self.out.items():
                subs = value.split()
                item = getitem(data, subs[0])
                for sub in subs[1:]:
                    item = getitem(item, sub)
                output[name] = item
        except KeyError as exc:
            raise APIException(f'Filter failed: key "{exc.args[0]}" not found in [{data}]! '
                               f'Maybe consider implement a validation if this is related with the api!') from None
        return output

    def __eq__(self, other: 'Filter') -> bool: return self.out == other.out

    def __str__(self) -> str: return f'Filter[{self.out}]'

    def __repr__(self) -> str: return str(self)


if __name__ == '__main__': pass
