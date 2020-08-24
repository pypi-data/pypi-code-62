#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : alikeypair.py
# @Author: encircles
# @Date  : 8/19/2020
# @Desc  :
from abc import ABCMeta, abstractmethod


class AliKeyPair(metaclass=ABCMeta):
    # SSH密钥对
    # CreateKeyPair	调用CreateKeyPair创建一对SSH密钥对。我们会为您保管密钥的公钥部分，并返回未加密的PEM编码的PKCS#8格式私钥。您需要自行妥善保管私钥部分。
    @abstractmethod
    def CreateKeyPair(self, params_json_str="{}") -> dict:
        pass

    # ImportKeyPair	调用ImportKeyPair导入由其他工具产生的RSA密钥对的公钥部分。导入密钥对后，阿里云为您保管公钥部分，您需要自行妥善保存密钥对的私钥部分。
    @abstractmethod
    def ImportKeyPair(self, params_json_str="{}") -> dict:
        pass

    # AttachKeyPair	调用AttachKeyPair绑定一个SSH密钥对到一台或多台Linux实例。
    @abstractmethod
    def AttachKeyPair(self, params_json_str="{}") -> dict:
        pass

    # DetachKeyPair	调用DetachKeyPair为一台或者多台Linux实例解绑SSH密钥对。
    @abstractmethod
    def DetachKeyPair(self, params_json_str="{}") -> dict:
        pass

    # DeleteKeyPairs	调用DeleteKeyPairs删除一对或者多对SSH密钥对。删除SSH密钥对后，我们不再为您保存该SSH密钥对，但是已经绑定的实例可以正常使用该SSH密钥对，其SSH密钥对名称仍然显示在实例详情中。
    @abstractmethod
    def DeleteKeyPairs(self, params_json_str="{}") -> dict:
        pass

    # DescribeKeyPairs	调用DescribeKeyPairs查询一个或多个密钥对。
    @abstractmethod
    def DescribeKeyPairs(self, params_json_str="{}") -> dict:
        pass
