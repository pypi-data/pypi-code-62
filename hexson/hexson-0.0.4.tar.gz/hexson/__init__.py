#!/usr/bin/env python3
# Json library support hex escape.
from .dumpper import Dumpper
from .parser import Parser
from .serializer import JSONSerializer


VERSION = (0, 0, 3)
__version__ = VERSION
__versionstr__ = "0.0.3"


__all__ = [
    "dump",
    "load",
    "dumps",
    "loads",
    "JSONSerializer"
]


def dump(input_obj, fd):
    """ Convert an Python type to a JSON string and write to a file. """
    fd.write(Dumpper(input_obj).dump_to_json())


def load(fd, utf_8_string=False):
    """ Read from a file and convert a JSON string to an Python type. """
    return Parser(fd.read()).parse_from_json(utf_8_string)


def dumps(input_obj):
    """ Convert an Python type to a JSON string. """
    return Dumpper(input_obj).dump_to_json()


def loads(input_json, utf_8_string=False):
    """ Convert a JSON string to an Python type. """
    return Parser(input_json).parse_from_json(utf_8_string)
