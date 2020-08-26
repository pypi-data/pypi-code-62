# -*- coding: utf-8 -*-
# Copyright (c) 2016, 2017, 2018, 2019 Sqreen. All rights reserved.
# Please refer to our terms for more information:
#
#     https://www.sqreen.io/terms.html
#
""" Web Application Firewall Binding
"""
import json
import ctypes

from ._compat import UNICODE_CLASS
from ._ffi import PW_BLOCK, PW_MONITOR, powerwaf_initWithDiag, powerwaf_freeDiagnotics, \
    powerwaf_run, powerwaf_clearRule, powerwaf_freeReturn, powerwaf_getVersion
from .input import Input


def initialize_with_diag(rule_name, rule_data):
    """ Initialize a WAF rule with diagnostic.
    """

    if isinstance(rule_name, UNICODE_CLASS):
        rule_name = rule_name.encode("utf-8", errors="surrogatepass")

    if isinstance(rule_data, UNICODE_CLASS):
        rule_data = rule_data.encode("utf-8", errors="surrogatepass")

    if rule_name is not None and not isinstance(rule_name, bytes):
        raise ValueError("rule_name must be a string, bytes or None")

    if not isinstance(rule_data, bytes):
        raise ValueError("rule_data must be a string or bytes")

    diag = None
    diag_ptr = ctypes.c_char_p(None)
    try:
        ret = powerwaf_initWithDiag(
            rule_name, rule_data, None, ctypes.byref(diag_ptr))
        if diag_ptr:
            diag = json.loads(diag_ptr.value.decode("utf-8"))
        return ret, diag
    finally:
        if diag_ptr:
            powerwaf_freeDiagnotics(diag_ptr)


def initialize(rule_name, rule_data):
    """ Initialize a WAF rule.
    """
    return initialize_with_diag(rule_name, rule_data)[0]


def validate(rule_data):
    """ Ask PowerWAF to parse and validate a ruleset.
    """
    return initialize_with_diag(None, rule_data)[1]


def clear(rule_name):
    """ Clear a WAF rule.
    """
    if isinstance(rule_name, UNICODE_CLASS):
        rule_name = rule_name.encode("utf-8", errors="surrogatepass")

    if not isinstance(rule_name, bytes):
        raise ValueError("rule_name must be a string or bytes")

    powerwaf_clearRule(rule_name)


def get_version():
    """ Get the WAF runtime version.
    """
    ver = powerwaf_getVersion()
    return int(ver.major), int(ver.minor), int(ver.patch)


def run(rule_name, parameters, budget):
    """ Run a WAF rule.
    """
    if isinstance(rule_name, UNICODE_CLASS):
        rule_name = rule_name.encode("utf-8", errors="surrogatepass")

    if not isinstance(rule_name, bytes):
        raise ValueError("rule_name must be a string or bytes")

    if not isinstance(parameters, Input):
        parameters = Input.from_python(parameters)

    return Return(powerwaf_run(
        rule_name, ctypes.byref(parameters._obj), ctypes.c_size_t(budget)))


def free(result):
    """ Free the result of the run function.
    """
    powerwaf_freeReturn(result)


class Return:
    """
    Higher-level WAF return value.
    """

    def __init__(self, obj):
        self._obj = obj

    def __del__(self):
        if self._obj is None:
            return
        free(self._obj)
        self._obj = None

    @property
    def action(self):
        if self._obj is not None and self._obj[0]:
            return self._obj[0].action

    @property
    def data(self):
        if self._obj is not None and self._obj[0]:
            return self._obj[0].data

    def __repr__(self):
        return "<Return action={0.action!r} data={0.data!r}>".format(self)
