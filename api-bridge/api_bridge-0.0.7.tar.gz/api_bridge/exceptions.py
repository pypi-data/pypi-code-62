#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2020-08-15"
__version__ = "0.0.7"

__all__ = ('APIException', 'RequestException', 'ValidationException', 'FilterException', 'URLException',)


EXCEPTIONS: bool = True


class APIException(Exception):
    @classmethod
    def raise_from(cls, *args):
        if EXCEPTIONS: raise cls(*args)


class RequestException(APIException): pass


class ValidationException(APIException): pass


class FilterException(APIException): pass


class URLException(APIException): pass


if __name__ == '__main__': pass
