#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : alihosts.py
# @Author: encircles
# @Date  : 8/19/2020
# @Desc  :
from abc import ABCMeta, abstractmethod


class AliHosts(metaclass=ABCMeta):
    # 专有宿主机
    # AllocateDedicatedHosts	调用AllocateDedicatedHosts创建一台或多台按量付费或者包年包月专有宿主机。专有宿主机是单租户独享的物理机资源，您可以在专有宿主机上自行创建ECS实例和获取物理服务器属性等信息。
    @abstractmethod
    def AllocateDedicatedHosts(self, params_json_str) -> dict:
        pass

    # RenewDedicatedHosts	调用RenewDedicatedHosts续费一台或者多台包年包月专有宿主机。
    @abstractmethod
    def RenewDedicatedHosts(self, params_json_str) -> dict:
        pass

    # ReleaseDedicatedHost	调用ReleaseDedicatedHost释放一台按量付费专有宿主机。
    @abstractmethod
    def ReleaseDedicatedHost(self, params_json_str) -> dict:
        pass

    # RedeployDedicatedHost	调用RedeployDedicatedHost执行专有宿主机的故障迁移。
    @abstractmethod
    def RedeployDedicatedHost(self, params_json_str) -> dict:
        pass

    # DescribeDedicatedHosts	调用DescribeDedicatedHosts查询一台或多台专有宿主机的详细信息，包括专有宿主机的物理性能指标、机器码、使用状态和已创建的ECS实例列表等。
    @abstractmethod
    def DescribeDedicatedHosts(self, params_json_str) -> dict:
        pass

    # DescribeDedicatedHostTypes	调用DescribeDedicatedHostTypes查询指定地域下支持的专有宿主机规格详细参数，或者查询专有宿主机支持的ECS实例规格族。
    @abstractmethod
    def DescribeDedicatedHostTypes(self, params_json_str) -> dict:
        pass

    # DescribeDedicatedHostAutoRenew	调用DescribeDedicatedHostAutoRenew查询一台或多台包年包月专有宿主机自动续费状态。
    @abstractmethod
    def DescribeDedicatedHostAutoRenew(self, params_json_str) -> dict:
        pass

    # ModifyInstanceDeployment	调用ModifyInstanceDeployment修改ECS实例的宿主机。ECS实例与目标宿主机必须位于同一地域。
    @abstractmethod
    def ModifyInstanceDeployment(self, params_json_str) -> dict:
        pass

    # ModifyDedicatedHostAttribute	调用ModifyDedicatedHostAttribute修改一台专有宿主机的部分信息，包括专有宿主机的名称、描述和服务不可用属性等。
    @abstractmethod
    def ModifyDedicatedHostAttribute(self, params_json_str) -> dict:
        pass

    # ModifyDedicatedHostAutoReleaseTime	调用ModifyDedicatedHostAutoReleaseTime为一台按量付费专有宿主机设定自动释放时间，或者取消自动释放一台按量付费专有宿主机。
    @abstractmethod
    def ModifyDedicatedHostAutoReleaseTime(self, params_json_str) -> dict:
        pass

    # ModifyDedicatedHostAutoRenewAttribute	调用ModifyDedicatedHostAutoRenewAttribute为一台或多台包年包月专有宿主机设置自动续费，也可以取消已设定的自动续费。
    @abstractmethod
    def ModifyDedicatedHostAutoRenewAttribute(self, params_json_str) -> dict:
        pass

    # ModifyDedicatedHostsChargeType	调用ModifyDedicatedHostsChargeType修改专有宿主机的付费类型。
    @abstractmethod
    def ModifyDedicatedHostsChargeType(self, params_json_str) -> dict:
        pass
