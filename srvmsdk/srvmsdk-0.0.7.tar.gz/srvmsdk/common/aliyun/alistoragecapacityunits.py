#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : alistoragecapacityunits.py
# @Author: encircles
# @Date  : 8/19/2020
# @Desc  :
from abc import ABCMeta, abstractmethod


class AliStorageCapacityUnits(metaclass=ABCMeta):
    # 存储容量单位包
    # PurchaseStorageCapacityUnit	调用PurchaseStorageCapacityUnit购买一个或多个存储容量单位包SCU（Storage Capacity Unit）。
    @abstractmethod
    def PurchaseStorageCapacityUnit(self, params_json_str) -> dict:
        pass

    # ModifyStorageCapacityUnitAttribute	调用ModifyStorageCapacityUnitAttribute修改一个存储容量单位包SCU的名称或者描述信息。
    @abstractmethod
    def ModifyStorageCapacityUnitAttribute(self, params_json_str) -> dict:
        pass

    # DescribeStorageCapacityUnits	调用DescribeStorageCapacityUnits查询一个或多个存储容量单位包SCU的详细信息。
    @abstractmethod
    def DescribeStorageCapacityUnits(self, params_json_str) -> dict:
        pass
