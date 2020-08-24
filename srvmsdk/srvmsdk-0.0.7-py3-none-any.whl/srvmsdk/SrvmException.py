#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : SrvmException.py
# @Author: encircles
# @Date  : 8/19/2020
# @Desc  :
import sys

from srvmsdk.common.errcode import getErrMsg


class SrvmException(Exception):
    """srvm sdk 异常类"""

    def __init__(self, code=None, message=None, requestId=None):
        self.code = code
        if message is None:
            message = getErrMsg(code)
        self.message = message
        self.requestId = requestId

    def __str__(self):
        s = "[Srvm Exception] code:%s message:%s requestId:%s" % (
            self.code, self.message, self.requestId)
        if sys.version_info[0] < 3 and isinstance(s, str):
            return s.encode("utf8")
        else:
            return s

    def get_code(self):
        return self.code

    def get_message(self):
        return self.message

    def get_request_id(self):
        return self.requestId
