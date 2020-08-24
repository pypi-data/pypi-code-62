#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : alibase.py
# @Author: encircles
# @Date  : 8/19/2020
# @Desc  :
from abc import ABCMeta

from srvmsdk.SrvmException import SrvmException
from srvmsdk.common import errcode
from srvmsdk.common.commonbase import CommonBase


class AliCommonBase(CommonBase, metaclass=ABCMeta):
    _accessKeyId = None
    _accessKeySecret = None

    def __init__(self, access_key_id, access_key_secret):
        self._accessKeyId = access_key_id
        self._accessKeySecret = access_key_secret

    def setAccessKey(self, access_key_id, access_key_secret):
        self._accessKeyId = access_key_id
        self._accessKeySecret = access_key_secret

    def getAccessKeyId(self):
        if self._accessKeyId is None:
            raise SrvmException(errcode.AL_ID_IS_NONE)
        return self._accessKeyId

    def getAccessKeySecret(self):
        if self._accessKeySecret is None:
            raise SrvmException(errcode.AL_SECRET_IS_NONE)
        return self._accessKeySecret
