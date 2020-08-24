#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : aliinstances.py
# @Author: encircles
# @Date  : 8/19/2020
# @Desc  :
from abc import ABCMeta, abstractmethod


class AliInstances(metaclass=ABCMeta):
    # RunInstances	调用RunInstances创建一台或多台按量付费或者包年包月ECS实例。
    @abstractmethod
    def RunInstances(self, params_json_str="{}") -> dict:
        pass

    # StartInstances	调用StartInstances启动一台或多台处于已停止（Stopped）状态的ECS实例。
    @abstractmethod
    def StartInstances(self, params_json_str="{}") -> dict:
        pass

    # StopInstances	调用StopInstances停止一台或多台运行中（Running）的ECS实例。
    @abstractmethod
    def StopInstances(self, params_json_str="{}") -> dict:
        pass

    # RebootInstances	调用RebootInstances重启一台或多台处于运行中（Running）状态的ECS实例。
    @abstractmethod
    def RebootInstances(self, params_json_str="{}") -> dict:
        pass

    # AttachInstanceRamRole	调用AttachInstanceRamRole为一台或多台ECS实例授予实例RAM角色。如果实例已有RAM角色，则报错提示您不能附加新的角色。
    @abstractmethod
    def AttachInstanceRamRole(self, params_json_str="{}") -> dict:
        pass

    # DetachInstanceRamRole	调用DetachInstanceRamRole收回一台或多台ECS实例的实例RAM角色。
    @abstractmethod
    def DetachInstanceRamRole(self, params_json_str="{}") -> dict:
        pass

    # DescribeInstanceStatus	调用DescribeInstanceStatus获取一台或多台ECS实例的状态信息。
    @abstractmethod
    def DescribeInstanceStatus(self, params_json_str="{}") -> dict:
        pass

    # DescribeInstances	调用DescribeInstances查询一台或多台ECS实例的详细信息。
    @abstractmethod
    def DescribeInstances(self, params_json_str="{}") -> dict:
        pass

    # DescribeInstanceVncUrl	调用DescribeInstanceVncUrl查询一台ECS实例的Web管理终端地址。
    @abstractmethod
    def DescribeInstanceVncUrl(self, params_json_str="{}") -> dict:
        pass

    # DescribeUserData	调用DescribeUserData查询一台ECS实例的自定义数据。
    @abstractmethod
    def DescribeUserData(self, params_json_str="{}") -> dict:
        pass

    # DescribeInstanceAutoRenewAttribute	调用DescribeInstanceAutoRenewAttribute查询一台或多台包年包月ECS实例自动续费状态。
    @abstractmethod
    def DescribeInstanceAutoRenewAttribute(self, params_json_str="{}") -> dict:
        pass

    # DescribeInstanceRamRole	调用DescribeInstanceRamRole查询一台或者多台ECS实例上的已赋予的实例RAM角色。
    @abstractmethod
    def DescribeInstanceRamRole(self, params_json_str="{}") -> dict:
        pass

    # DescribeSpotPriceHistory	调用DescribeSpotPriceHistory查询抢占式实例近30天内的历史价格。
    @abstractmethod
    def DescribeSpotPriceHistory(self, params_json_str="{}") -> dict:
        pass

    # DescribeInstanceTypeFamilies	调用DescribeInstanceTypeFamilies查询云服务器ECS提供的实例规格族资源。
    @abstractmethod
    def DescribeInstanceTypeFamilies(self, params_json_str="{}") -> dict:
        pass

    # DescribeInstanceTypes	调用DescribeInstanceTypes查询云服务器ECS提供的实例规格资源。
    @abstractmethod
    def DescribeInstanceTypes(self, params_json_str="{}") -> dict:
        pass

    # ModifyInstanceAttribute	调用ModifyInstanceAttribute修改一台ECS实例的部分信息，包括实例密码、名称、描述、主机名和自定义数据等。如果是突发性能实例，可以切换这台实例的性能突发模式。
    @abstractmethod
    def ModifyInstanceAttribute(self, params_json_str="{}") -> dict:
        pass

    # ModifyInstanceVncPasswd	调用ModifyInstanceVncPasswd修改一台ECS实例的Web管理终端密码。
    @abstractmethod
    def ModifyInstanceVncPasswd(self, params_json_str="{}") -> dict:
        pass

    # ModifyInstanceAutoReleaseTime	调用ModifyInstanceAutoReleaseTime为一台按量付费ECS实例设定或者取消自动释放时间。设置自动释放时请谨慎操作，配置的时间到期后将自动释放ECS实例。
    @abstractmethod
    def ModifyInstanceAutoReleaseTime(self, params_json_str="{}") -> dict:
        pass

    # ModifyInstanceAutoRenewAttribute	调用ModifyInstanceAutoRenewAttribute设置一台或多台包年包月实例的自动续费状态。为了减少您的资源到期维护成本，包年包月ECS实例可以设置自动续费。
    @abstractmethod
    def ModifyInstanceAutoRenewAttribute(self, params_json_str="{}") -> dict:
        pass

    # ModifyInstanceChargeType	调用ModifyInstanceChargeType更换一台或者多台ECS实例的计费方式。支持在按量付费实例和包年包月实例间相互转换，同时可以将实例挂载的所有按量付费云盘转换为包年包月云盘。
    @abstractmethod
    def ModifyInstanceChargeType(self, params_json_str="{}") -> dict:
        pass

    # ModifyInstanceSpec	调用ModifyInstanceSpec调整一台按量付费ECS实例的实例规格和公网带宽大小。
    @abstractmethod
    def ModifyInstanceSpec(self, params_json_str="{}") -> dict:
        pass

    # ModifyPrepayInstanceSpec	调用ModifyPrepayInstanceSpec升级或者降低一台包年包月ECS实例的实例规格，新实例规格将会覆盖实例的整个生命周期。
    @abstractmethod
    def ModifyPrepayInstanceSpec(self, params_json_str="{}") -> dict:
        pass

    # ModifyInstanceMetadataOptions	调用ModifyInstanceMetadataOptions修改一台实例的元数据信息。
    @abstractmethod
    def ModifyInstanceMetadataOptions(self, params_json_str="{}") -> dict:
        pass

    # RenewInstance	调用RenewInstance续费一台包年包月ECS实例。
    @abstractmethod
    def RenewInstance(self, params_json_str="{}") -> dict:
        pass

    # ReactivateInstances	重新启动一台已过期或欠费回收中的按量付费ECS实例。
    @abstractmethod
    def ReactivateInstances(self, params_json_str="{}") -> dict:
        pass

    # StartInstance	调用StartInstance启动一台实例。
    @abstractmethod
    def StartInstance(self, params_json_str="{}") -> dict:
        pass

    # StopInstance	调用StopInstance停止运行一台实例。
    @abstractmethod
    def StopInstance(self, params_json_str="{}") -> dict:
        pass

    # RebootInstance	当一台ECS实例处于运行中（Running）状态时，调用RebootInstance可以重启这台实例。
    @abstractmethod
    def RebootInstance(self, params_json_str="{}") -> dict:
        pass

    # CreateInstance	调用CreateInstance创建一台包年包月或者按量付费ECS实例。
    @abstractmethod
    def CreateInstance(self, params_json_str="{}") -> dict:
        pass

    # DeleteInstance	调用DeleteInstance释放一台按量付费实例或者到期的包年包月实例。
    @abstractmethod
    def DeleteInstance(self, params_json_str="{}") -> dict:
        pass

    # DeleteInstances	调用DeleteInstances释放一台或多台按量付费ECS实例或者到期的包年包月ECS实例。
    @abstractmethod
    def DeleteInstances(self, params_json_str="{}") -> dict:
        pass
