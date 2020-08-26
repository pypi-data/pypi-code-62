# -*- coding: utf-8 -*-
# Copyright (c) 2016, 2017, 2018, 2019 Sqreen. All rights reserved.
# Please refer to our terms for more information:
#
#     https://www.sqreen.io/terms.html
#
""" Binding for the WAF Input Data Structure
"""
import ctypes

from ._compat import UNICODE_CLASS
from ._ffi import powerwaf_createArray, powerwaf_createInt, powerwaf_createUint, \
    powerwaf_createMap, powerwaf_createStringWithLength, powerwaf_addToPWArgsArray, \
    powerwaf_addToPWArgsMap, powerwaf_freeInput


def create_array():
    return powerwaf_createArray()


def create_int(value):
    return powerwaf_createInt(ctypes.c_int64(value))


def create_uint(value):
    return powerwaf_createUint(ctypes.c_uint64(value))


def create_map():
    return powerwaf_createMap()


def create_string(value, max_string_length=4096):
    if isinstance(value, UNICODE_CLASS):
        value = value[:max_string_length].encode("utf-8", errors="surrogatepass")

    if not isinstance(value, bytes):
        raise ValueError("value must be a string or bytes")

    value = value[:max_string_length]
    return powerwaf_createStringWithLength(value, len(value))


def append_to_array(array, value):
    return powerwaf_addToPWArgsArray(ctypes.byref(array), value)


def append_to_map(array, key, value):
    if isinstance(key, UNICODE_CLASS):
        key = key.encode("utf-8", errors="surrogatepass")

    if not isinstance(key, bytes):
        raise ValueError("value must be a string or bytes")

    return powerwaf_addToPWArgsMap(ctypes.byref(array), key, 0, value)


def free(value):
    powerwaf_freeInput(ctypes.byref(value), False)


def create(value, max_depth=10, ignore_none=True, max_string_length=4096,
           max_items=150):
    """ Lower-level function to convert a Python value to input value
    """
    if isinstance(value, str) or isinstance(value, bytes):
        return create_string(value, max_string_length=max_string_length)

    if isinstance(value, bool):
        return create_uint(int(value))

    if isinstance(value, int):
        if value < 0:
            return create_int(value)
        else:
            return create_uint(value)

    if isinstance(value, list) or isinstance(value, tuple):
        obj = create_array()
        if max_depth <= 0:
            # ignore if deeply nested
            return obj
        for i, item in enumerate(value):
            if i >= max_items or (item is None and ignore_none):
                continue
            item_obj = create(item, max_depth=max_depth - 1)
            ret = append_to_array(obj, item_obj)
            if ret is False:
                free(item_obj)
        return obj

    if isinstance(value, dict):
        obj = create_map()
        if max_depth <= 0:
            # ignore if deeply nested
            return obj
        for i, (k, v) in enumerate(value.items()):
            if i >= max_items or (v is None and ignore_none):
                continue
            item_obj = create(v, max_depth=max_depth - 1)
            ret = append_to_map(obj, k, item_obj)
            if ret is False:
                free(item_obj)
        return obj

    return create_string(UNICODE_CLASS(value), max_string_length=max_string_length)


class Input:
    """
    Higher-level bridge between Python values and input values (PWArgs).
    """

    def __init__(self, obj):
        self._obj = obj

    def __del__(self):
        if self._obj is None:
            return
        free(self._obj)
        self._obj = None

    @classmethod
    def from_python(cls, value, **kwargs):
        """ Convert a Python value to a managed input.
        """
        return cls(create(value, **kwargs))

    def __repr__(self):
        return "<{} obj={!r}>".format(self.__class__.__name__, self._obj)


# Alias for versions <1.0
PWArgs = Input

__all__ = ["Input"]
