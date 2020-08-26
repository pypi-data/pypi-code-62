# -*- coding: utf-8 -*-
# Copyright (c) 2016 - 2020 Sqreen. All rights reserved.
# Please refer to our terms for more information:
# 
#     https://www.sqreen.io/terms.html
# 
# /!\ This file is generated. DO NOT EDIT /!\
from ctypes import *

from ._ffi import _lib, _PWArgs, PW_LOG_FUNC

PWI_INVALID = 0
PWI_SIGNED_NUMBER = 1 << 0
PWI_UNSIGNED_NUMBER = 1 << 1
PWI_STRING = 1 << 2
PWI_ARRAY = 1 << 3
PWI_MAP = 1 << 4

PW_INPUT_TYPE = c_int

PWArgs = _PWArgs

class PWConfig(Structure):
    _fields_ = [
        ("maxArrayLength", c_uint64),
        ("maxMapDepth", c_uint64),
    ]

_powerwaf_init = _lib.powerwaf_init
_powerwaf_init.restype = c_bool
_powerwaf_init.argtypes = [c_char_p, c_char_p, POINTER(PWConfig)]
def powerwaf_init(ruleName, wafRule, config):
    # type: (Any, Any, Any) -> c_bool
    return _powerwaf_init(ruleName, wafRule, config)  # type: ignore

PWD_PARSING_JSON = 0
PWD_PARSING_RULE = 1
PWD_PARSING_RULE_FILTER = 2
PWD_OPERATOR_VALUE = 3
PWD_DUPLICATE_RULE = 4
PWD_PARSING_FLOW = 5
PWD_PARSING_FLOW_STEP = 6
PWD_MEANINGLESS_STEP = 7
PWD_DUPLICATE_FLOW = 8
PWD_DUPLICATE_FLOW_STEP = 9

PW_DIAG_CODE = c_int

_powerwaf_initWithDiag = _lib.powerwaf_initWithDiag
_powerwaf_initWithDiag.restype = c_bool
_powerwaf_initWithDiag.argtypes = [c_char_p, c_char_p, POINTER(PWConfig), POINTER(c_char_p)]
def powerwaf_initWithDiag(ruleName, wafRule, config, errors):
    # type: (Any, Any, Any, Any) -> c_bool
    return _powerwaf_initWithDiag(ruleName, wafRule, config, errors)  # type: ignore

_powerwaf_freeDiagnotics = _lib.powerwaf_freeDiagnotics
_powerwaf_freeDiagnotics.restype = None
_powerwaf_freeDiagnotics.argtypes = [c_char_p]
def powerwaf_freeDiagnotics(errors):
    # type: (Any) -> None
    return _powerwaf_freeDiagnotics(errors)  # type: ignore

_powerwaf_clearRule = _lib.powerwaf_clearRule
_powerwaf_clearRule.restype = None
_powerwaf_clearRule.argtypes = [c_char_p]
def powerwaf_clearRule(ruleName):
    # type: (Any) -> None
    return _powerwaf_clearRule(ruleName)  # type: ignore

_powerwaf_clearAll = _lib.powerwaf_clearAll
_powerwaf_clearAll.restype = None
_powerwaf_clearAll.argtypes = []
def powerwaf_clearAll():
    # type: () -> None
    return _powerwaf_clearAll()  # type: ignore

PW_ERR_INTERNAL = -6
PW_ERR_TIMEOUT = -5
PW_ERR_INVALID_CALL = -4
PW_ERR_INVALID_RULE = -3
PW_ERR_INVALID_FLOW = -2
PW_ERR_NORULE = -1
PW_GOOD = 0
PW_MONITOR = 1
PW_BLOCK = 2

PW_RET_CODE = c_int

class PWRet(Structure):
    _fields_ = [
        ("action", PW_RET_CODE),
        ("data", c_char_p),
    ]

_powerwaf_run = _lib.powerwaf_run
_powerwaf_run.restype = POINTER(PWRet)
_powerwaf_run.argtypes = [c_char_p, POINTER(PWArgs), c_size_t]
def powerwaf_run(ruleName, parameters, timeLeftInUs):
    # type: (Any, Any, Any) -> pointer
    return _powerwaf_run(ruleName, parameters, timeLeftInUs)  # type: ignore

class PWVersion(Structure):
    _fields_ = [
        ("major", c_uint16),
        ("minor", c_uint16),
        ("patch", c_uint16),
    ]

_powerwaf_getVersion = _lib.powerwaf_getVersion
_powerwaf_getVersion.restype = PWVersion
_powerwaf_getVersion.argtypes = []
def powerwaf_getVersion():
    # type: () -> PWVersion
    return _powerwaf_getVersion()  # type: ignore

PWL_TRACE = 0
PWL_DEBUG = 1
PWL_INFO = 2
PWL_WARN = 3
PWL_ERROR = 4
_PWL_AFTER_LAST = 5

PW_LOG_LEVEL = c_int

_powerwaf_setupLogging = _lib.powerwaf_setupLogging
_powerwaf_setupLogging.restype = c_bool
_powerwaf_setupLogging.argtypes = [PW_LOG_FUNC, PW_LOG_LEVEL]
def powerwaf_setupLogging(cb, min_level):
    # type: (Any, Any) -> c_bool
    return _powerwaf_setupLogging(cb, min_level)  # type: ignore

_powerwaf_getInvalidPWArgs = _lib.powerwaf_getInvalidPWArgs
_powerwaf_getInvalidPWArgs.restype = PWArgs
_powerwaf_getInvalidPWArgs.argtypes = []
def powerwaf_getInvalidPWArgs():
    # type: () -> PWArgs
    return _powerwaf_getInvalidPWArgs()  # type: ignore

_powerwaf_createStringWithLength = _lib.powerwaf_createStringWithLength
_powerwaf_createStringWithLength.restype = PWArgs
_powerwaf_createStringWithLength.argtypes = [c_char_p, c_size_t]
def powerwaf_createStringWithLength(string, length):
    # type: (Any, Any) -> PWArgs
    return _powerwaf_createStringWithLength(string, length)  # type: ignore

_powerwaf_createString = _lib.powerwaf_createString
_powerwaf_createString.restype = PWArgs
_powerwaf_createString.argtypes = [c_char_p]
def powerwaf_createString(string):
    # type: (Any) -> PWArgs
    return _powerwaf_createString(string)  # type: ignore

_powerwaf_createInt = _lib.powerwaf_createInt
_powerwaf_createInt.restype = PWArgs
_powerwaf_createInt.argtypes = [c_int64]
def powerwaf_createInt(value):
    # type: (Any) -> PWArgs
    return _powerwaf_createInt(value)  # type: ignore

_powerwaf_createUint = _lib.powerwaf_createUint
_powerwaf_createUint.restype = PWArgs
_powerwaf_createUint.argtypes = [c_uint64]
def powerwaf_createUint(value):
    # type: (Any) -> PWArgs
    return _powerwaf_createUint(value)  # type: ignore

_powerwaf_createArray = _lib.powerwaf_createArray
_powerwaf_createArray.restype = PWArgs
_powerwaf_createArray.argtypes = []
def powerwaf_createArray():
    # type: () -> PWArgs
    return _powerwaf_createArray()  # type: ignore

_powerwaf_createMap = _lib.powerwaf_createMap
_powerwaf_createMap.restype = PWArgs
_powerwaf_createMap.argtypes = []
def powerwaf_createMap():
    # type: () -> PWArgs
    return _powerwaf_createMap()  # type: ignore

_powerwaf_addToPWArgsArray = _lib.powerwaf_addToPWArgsArray
_powerwaf_addToPWArgsArray.restype = c_bool
_powerwaf_addToPWArgsArray.argtypes = [POINTER(PWArgs), PWArgs]
def powerwaf_addToPWArgsArray(array, entry):
    # type: (Any, Any) -> c_bool
    return _powerwaf_addToPWArgsArray(array, entry)  # type: ignore

_powerwaf_addToPWArgsMap = _lib.powerwaf_addToPWArgsMap
_powerwaf_addToPWArgsMap.restype = c_bool
_powerwaf_addToPWArgsMap.argtypes = [POINTER(PWArgs), c_char_p, c_size_t, PWArgs]
def powerwaf_addToPWArgsMap(map, entryName, entryNameLength, entry):
    # type: (Any, Any, Any, Any) -> c_bool
    return _powerwaf_addToPWArgsMap(map, entryName, entryNameLength, entry)  # type: ignore

_powerwaf_freeInput = _lib.powerwaf_freeInput
_powerwaf_freeInput.restype = None
_powerwaf_freeInput.argtypes = [POINTER(PWArgs), c_bool]
def powerwaf_freeInput(input, freeSelf):
    # type: (Any, Any) -> None
    return _powerwaf_freeInput(input, freeSelf)  # type: ignore

_powerwaf_freeReturn = _lib.powerwaf_freeReturn
_powerwaf_freeReturn.restype = None
_powerwaf_freeReturn.argtypes = [POINTER(PWRet)]
def powerwaf_freeReturn(output):
    # type: (Any) -> None
    return _powerwaf_freeReturn(output)  # type: ignore
