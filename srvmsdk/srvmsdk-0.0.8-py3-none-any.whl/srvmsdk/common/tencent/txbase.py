#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : alibase.py
# @Author: encircles
# @Date  : 8/18/2020
# @Desc  :
from abc import ABCMeta, abstractmethod

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.cvm.v20170312 import cvm_client

from srvmsdk.SrvmException import SrvmException
from srvmsdk.common import errcode

from srvmsdk.common.commonbase import CommonBase
from srvmsdk.common.tencent.txregion import TxRegion
from srvmsdk.common.tencent.txinstances import TxInstances
from srvmsdk.common.tencent.tximages import TxImages
from srvmsdk.common.tencent.txkeypair import TxKeyPair
from srvmsdk.common.tencent.txhosts import TxHosts
from srvmsdk.common.tencent.txsecuritygroups import TxSecurityGroups
from srvmsdk.common.tencent.txinternet import TxInternet
from srvmsdk.common.tencent.txrecovergroups import TxRecoverGroups


class TxCommonBase(
    TxRegion,
    TxInstances,

    TxImages,
    TxKeyPair,
    TxHosts,
    TxSecurityGroups,
    TxInternet,
    TxRecoverGroups,

    CommonBase,
    metaclass=ABCMeta,
):
    _secretId = None
    _secretKey = None
    _region = None
    _endpoint = "cvm.tencentcloudapi.com"

    """认证对象"""
    cred = None
    """client 对象"""
    client = None

    def __init__(self, secret_id, secret_key, region, **kwargs):
        self._secretId = secret_id
        self._secretKey = secret_key
        self._region = region

        # 实例化一个认证对象，入参需要传入腾讯云账户 secretId，secretKey
        cred = credential.Credential(self.getSecretId(), self.getSecretKey())
        # 实例化要请求产品 (以 cvm 为例) 的 client 对象
        client = cvm_client.CvmClient(cred, self.getRegion())

        self.cred = cred
        self.client = client

    def setSecret(self, secret_id, secret_key, region):
        self._secretId = secret_id
        self._secretKey = secret_key
        self._region = region

    def setSecretId(self, secret_id):
        self._secretId = secret_id

    def setSecretKey(self, secret_key):
        self._secretKey = secret_key

    def setRegion(self, region):
        self._region = region

    def setEndpoint(self, endpoint):
        self._endpoint = endpoint

    def getSecretId(self):
        if self._secretId is None:
            raise SrvmException(errcode.TX_ID_IS_NONE)
        return self._secretId

    def getSecretKey(self):
        if self._secretKey is None:
            raise SrvmException(errcode.TX_KEY_IS_NONE)
        return self._secretKey

    def getRegion(self):
        if self._region is None:
            raise SrvmException(errcode.TX_REGION_NONE)
        return self._region

    def getEndpoint(self):
        if self._endpoint is None:
            raise SrvmException(errcode.TX_ENDPOINT_NONE)
        return self._endpoint
