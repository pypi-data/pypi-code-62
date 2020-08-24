#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : alireservedinstances.py
# @Author: encircles
# @Date  : 8/19/2020
# @Desc  :
from abc import ABCMeta, abstractmethod


class AliReservedInstances(metaclass=ABCMeta):
    # 预留实例券
    # PurchaseReservedInstancesOffering	调用PurchaseReservedInstancesOffering购买一张预留实例券。预留实例券可以自动匹配对应的ECS实例，抵扣按量付费实例账单。
    @abstractmethod
    def PurchaseReservedInstancesOffering(self, params_json_str="{}") -> dict:
        pass

    # DescribeReservedInstances	调用DescribeReservedInstances查询已经购买的预留实例券。
    @abstractmethod
    def DescribeReservedInstances(self, params_json_str="{}") -> dict:
        pass

    # ModifyReservedInstances	您可以通过ModifyReservedInstances更改预留实例券。
    @abstractmethod
    def ModifyReservedInstances(self, params_json_str="{}") -> dict:
        pass
