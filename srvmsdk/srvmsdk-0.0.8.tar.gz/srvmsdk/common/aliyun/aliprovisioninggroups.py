#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : aliprovisioninggroups.py
# @Author: encircles
# @Date  : 8/19/2020
# @Desc  :
from abc import ABCMeta, abstractmethod


class AliProvisioningGroups(metaclass=ABCMeta):
    # 弹性供应组
    # CreateAutoProvisioningGroup	调用CreateAutoProvisioningGroup接口创建一个弹性供应组。
    @abstractmethod
    def CreateAutoProvisioningGroup(self, params_json_str="{}") -> dict:
        pass

    # ModifyAutoProvisioningGroup	调用ModifyAutoProvisioningGroup接口修改一个弹性供应组的设置。
    @abstractmethod
    def ModifyAutoProvisioningGroup(self, params_json_str="{}") -> dict:
        pass

    # DeleteAutoProvisioningGroup	调用DeleteAutoProvisioningGroup接口删除一个弹性供应组。
    @abstractmethod
    def DeleteAutoProvisioningGroup(self, params_json_str="{}") -> dict:
        pass

    # DescribeAutoProvisioningGroupInstances	调用DescribeAutoProvisioningGroupInstances查询指定弹性供应组下的实例。
    @abstractmethod
    def DescribeAutoProvisioningGroupInstances(self, params_json_str="{}") -> dict:
        pass

    # DescribeAutoProvisioningGroups	调用DescribeAutoProvisioningGroups接口查询弹性供应组。
    @abstractmethod
    def DescribeAutoProvisioningGroups(self, params_json_str="{}") -> dict:
        pass

    # DescribeAutoProvisioningGroupHistory	调用DescribeAutoProvisioningGroupHistory接口查询弹性供应组的调度任务信息。
    @abstractmethod
    def DescribeAutoProvisioningGroupHistory(self, params_json_str="{}") -> dict:
        pass
