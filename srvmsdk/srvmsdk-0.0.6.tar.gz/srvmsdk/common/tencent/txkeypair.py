#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : txkeypair.py
# @Author: encircles
# @Date  : 8/19/2020
# @Desc  :
from abc import ABCMeta, abstractmethod


class TxKeyPair(metaclass=ABCMeta):
    # region 密钥相关接口

    # CreateKeyPair	创建密钥对
    @abstractmethod
    def CreateKeyPair(self, params_json_str) -> dict:
        pass

    # DeleteKeyPairs	删除密钥对
    @abstractmethod
    def DeleteKeyPairs(self, params_json_str) -> dict:
        pass

    # ModifyKeyPairAttribute	修改密钥对属性
    @abstractmethod
    def ModifyKeyPairAttribute(self, params_json_str) -> dict:
        pass

    # AssociateInstancesKeyPairs	绑定密钥对
    @abstractmethod
    def AssociateInstancesKeyPairs(self, params_json_str) -> dict:
        pass

    # DisassociateInstancesKeyPairs	解绑密钥对
    @abstractmethod
    def DisassociateInstancesKeyPairs(self, params_json_str) -> dict:
        pass

    # DescribeKeyPairs	查询密钥对列表
    @abstractmethod
    def DescribeKeyPairs(self, params_json_str) -> dict:
        pass

    # ImportKeyPair	导入密钥对
    @abstractmethod
    def ImportKeyPair(self, params_json_str) -> dict:
        pass

    # endregion
