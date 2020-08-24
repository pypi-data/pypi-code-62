#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : txrecovergroups.py
# @Author: encircles
# @Date  : 8/19/2020
# @Desc  :
from abc import ABCMeta, abstractmethod


class TxRecoverGroups(metaclass=ABCMeta):

    # region 置放群组相关接口
    # CreateDisasterRecoverGroup	创建分散置放群组
    @abstractmethod
    def CreateDisasterRecoverGroup(self, params_json_str="{}") -> dict:
        pass

    # DeleteDisasterRecoverGroups	删除分散置放群组
    @abstractmethod
    def DeleteDisasterRecoverGroups(self, params_json_str="{}") -> dict:
        pass

    # DescribeDisasterRecoverGroupQuota	查询置放群组配额
    @abstractmethod
    def DescribeDisasterRecoverGroupQuota(self, params_json_str="{}") -> dict:
        pass

    # DescribeDisasterRecoverGroups	查询分散置放群组信息
    @abstractmethod
    def DescribeDisasterRecoverGroups(self, params_json_str="{}") -> dict:
        pass

    # ModifyDisasterRecoverGroupAttribute	修改分散置放群组属性
    @abstractmethod
    def ModifyDisasterRecoverGroupAttribute(self, params_json_str="{}") -> dict:
        pass
    # endregion
