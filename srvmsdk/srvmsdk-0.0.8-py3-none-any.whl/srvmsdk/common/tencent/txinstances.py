#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : txinstances.py
# @Author: encircles
# @Date  : 8/19/2020
# @Desc  :
from abc import ABCMeta, abstractmethod


class TxInstances(metaclass=ABCMeta):
    # region 实例相关 ==========================
    @abstractmethod
    def RunInstances(self, params_json_str="{}") -> dict:
        pass

    @abstractmethod
    def InquiryPriceRunInstances(self, params_json_str="{}") -> dict:
        pass

    @abstractmethod
    def StartInstances(self, params_json_str="{}") -> dict:
        pass

    # StopInstances	关闭实例
    @abstractmethod
    def StopInstances(self, params_json_str="{}") -> dict:
        pass

    # RebootInstances	重启实例
    @abstractmethod
    def RebootInstances(self, params_json_str="{}") -> dict:
        pass

    # ResetInstance	重装实例
    @abstractmethod
    def ResetInstance(self, params_json_str="{}") -> dict:
        pass

    # InquiryPriceResetInstance	重装实例询价
    @abstractmethod
    def InquiryPriceResetInstance(self, params_json_str="{}") -> dict:
        pass

    # ResetInstancesPassword	重置实例密码
    @abstractmethod
    def ResetInstancesPassword(self, params_json_str="{}") -> dict:
        pass

    # TerminateInstances	退还实例
    @abstractmethod
    def TerminateInstances(self, params_json_str="{}") -> dict:
        pass

    # DescribeInstances	查看实例列表
    @abstractmethod
    def DescribeInstances(self, params_json_str="{}") -> dict:
        pass

    # DescribeInstancesStatus	查看实例状态列表
    @abstractmethod
    def DescribeInstancesStatus(self, params_json_str="{}") -> dict:
        pass

    # ModifyInstancesAttribute	修改实例的属性
    @abstractmethod
    def ModifyInstancesAttribute(self, params_json_str="{}") -> dict:
        pass

    # ModifyInstancesProject	修改实例所属项目
    @abstractmethod
    def ModifyInstancesProject(self, params_json_str="{}") -> dict:
        pass

    # ResetInstancesType	调整实例配置
    @abstractmethod
    def ResetInstancesType(self, params_json_str="{}") -> dict:
        pass

    # InquiryPriceResetInstancesType	调整实例配置询价
    @abstractmethod
    def InquiryPriceResetInstancesType(self, params_json_str="{}") -> dict:
        pass

    # ResizeInstanceDisks	扩容实例磁盘
    @abstractmethod
    def ResizeInstanceDisks(self, params_json_str="{}") -> dict:
        pass

    # InquiryPriceResizeInstanceDisks	扩容实例磁盘询价
    @abstractmethod
    def InquiryPriceResizeInstanceDisks(self, params_json_str="{}") -> dict:
        pass

    # DescribeInstanceFamilyConfigs	查询所支持的实例机型族信息
    @abstractmethod
    def DescribeInstanceFamilyConfigs(self, params_json_str="{}") -> dict:
        pass

    # DescribeInstanceTypeConfigs	查询实例机型列表
    @abstractmethod
    def DescribeInstanceTypeConfigs(self, params_json_str="{}") -> dict:
        pass

    # RenewInstances	续费实例
    @abstractmethod
    def RenewInstances(self, params_json_str="{}") -> dict:
        pass

    # InquiryPriceRenewInstances	续费实例询价
    @abstractmethod
    def InquiryPriceRenewInstances(self, params_json_str="{}") -> dict:
        pass

    # ModifyInstancesRenewFlag	修改实例续费标识
    @abstractmethod
    def ModifyInstancesRenewFlag(self, params_json_str="{}") -> dict:
        pass

    # DescribeZoneInstanceConfigInfos	获取可用区机型配置信息
    @abstractmethod
    def DescribeZoneInstanceConfigInfos(self, params_json_str="{}") -> dict:
        pass

    # DescribeInstanceVncUrl	查询实例管理终端地址
    @abstractmethod
    def DescribeInstanceVncUrl(self, params_json_str="{}") -> dict:
        pass

    # DescribeInstancesOperationLimit	查询实例操作限制
    @abstractmethod
    def DescribeInstancesOperationLimit(self, params_json_str="{}") -> dict:
        pass

    # InquiryPriceModifyInstancesChargeType	修改实例计费模式询价
    @abstractmethod
    def InquiryPriceModifyInstancesChargeType(self, params_json_str="{}") -> dict:
        pass

    # ModifyInstancesChargeType
    @abstractmethod
    def ModifyInstancesChargeType(self, params_json_str="{}") -> dict:
        pass

    # endregion
