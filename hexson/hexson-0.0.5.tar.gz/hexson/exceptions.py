#!/usr/bin/env python3
# Json library support hex escape.


__all__ = [
    "HexsonDumpperException",
    "HexsonParserException"
]


class HexsonDumpperException(Exception):
    """ Exception happend in Dumpper. """


class HexsonParserException(Exception):
    """ Exception happend in Parser. """
