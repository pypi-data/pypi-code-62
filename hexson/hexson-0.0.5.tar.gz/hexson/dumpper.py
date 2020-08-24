#!/usr/bin/env python3
# Json library support hex escape.
from .exceptions import HexsonDumpperException
import json


class Dumpper(object):
    """ Json dumpper. """

    def __init__(self, input_obj):
        self.input_obj = input_obj

    def __is_printable_ascii(self, input_int):
        if input_int == 92 or input_int == 34:
            return False
        elif input_int >= 32 and input_int <= 126:
            return True
        else:
            return False

    def __quote(self, input_str):
        return json.dumps(input_str)

    def __bytes(self, input_bytes):
        ret = ''
        ret += '"'
        for byte in input_bytes:
            if self.__is_printable_ascii(byte):
                ret += chr(byte)
            elif byte == 34:
                ret += "\\\""
            elif byte == 92:
                ret += "\\\\"
            elif byte == 7:
                ret += "\\\\a"
            elif byte == 8:
                ret += "\\\\b"
            elif byte == 9:
                ret += "\\\\t"
            elif byte == 10:
                ret += "\\\\n"
            elif byte == 11:
                ret += "\\\\v"
            elif byte == 12:
                ret += "\\\\f"
            elif byte == 13:
                ret += "\\\\r"
            else:
                ret += "\\\\x%02x" % byte
        ret += '"'
        return ret

    def __pair(self, key_str, value_str):
        return '%s:%s' % (key_str, value_str)

    def __dict(self, obj):
        is_empty = True

        ret = ''
        ret += '{'
        for key in obj:
            if is_empty:
                is_empty = False
            else:
                ret += ','
            value = obj[key]
            ret += self.__pair(self.__quote(key), self.__value(value))

        ret += '}'
        return ret

    def __list(self, obj):
        is_empty = True

        ret = ''
        ret += '['
        for item in obj:
            if is_empty:
                is_empty = False
            else:
                ret += ','
            ret += self.__value(item)

        ret += ']'
        return ret

    def __value(self, obj):
        """ Convert an type in Python to object in JSON. """
        if isinstance(obj, int) or isinstance(obj, float):
            # Number type.
            return str(obj)
        elif isinstance(obj, str):
            # String type.
            return self.__quote(obj)
        elif isinstance(obj, bytes):
            # String type with hex escape.
            return self.__bytes(obj)
        elif isinstance(obj, dict):
            # Object type.
            return self.__dict(obj)
        elif isinstance(obj, list):
            # Array type.
            return self.__list(obj)
        elif obj is None:
            # Null.
            return 'null'
        elif obj is True:
            # True.
            return 'true'
        elif obj is False:
            # False.
            return 'false'
        else:
            raise HexsonDumpperException('The type of object is illegal: ' + self.input_obj)

    def dump_to_json(self):
        """ Called by outside. """
        return self.__value(self.input_obj)
