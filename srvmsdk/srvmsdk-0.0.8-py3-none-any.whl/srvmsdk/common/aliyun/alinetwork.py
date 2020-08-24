#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : alinetwork.py
# @Author: encircles
# @Date  : 8/19/2020
# @Desc  :
from abc import ABCMeta, abstractmethod


class AliNetwork(metaclass=ABCMeta):
    # 网络
    # ModifyInstanceVpcAttribute	调用ModifyInstanceVpcAttribute修改一台ECS实例的专有网络VPC属性。
    @abstractmethod
    def ModifyInstanceVpcAttribute(self, params_json_str="{}") -> dict:
        pass

    # AllocatePublicIpAddress	调用AllocatePublicIpAddress为一台ECS实例分配一个公网IP地址。
    @abstractmethod
    def AllocatePublicIpAddress(self, params_json_str="{}") -> dict:
        pass

    # ConvertNatPublicIpToEip	调用ConvertNatPublicIpToEip将一台网络类型为专有网络VPC的ECS实例的公网IP（NatPublicIp）转化为弹性公网IP（EIP）。
    @abstractmethod
    def ConvertNatPublicIpToEip(self, params_json_str="{}") -> dict:
        pass

    # AttachClassicLinkVpc	调用AttachClassicLinkVpc将一台经典网络类型实例连接到专有网络VPC中，使经典网络类型实例可以和VPC中的云资源私网互通。
    @abstractmethod
    def AttachClassicLinkVpc(self, params_json_str="{}") -> dict:
        pass

    # DetachClassicLinkVpc	调用DetachClassicLinkVpc取消经典网络类型实例与专有网络VPC的连接（ClassicLink）。取消ClassicLink后，经典网络类型实例无法与VPC互通。
    @abstractmethod
    def DetachClassicLinkVpc(self, params_json_str="{}") -> dict:
        pass

    # DescribeBandwidthLimitation	调用DescribeBandwidthLimitation查询带宽资源列表。
    @abstractmethod
    def DescribeBandwidthLimitation(self, params_json_str="{}") -> dict:
        pass

    # DescribeClassicLinkInstances	调用DescribeClassicLinkInstances查询一台或多台与专有网络VPC建立了连接的经典网络类型实例。
    @abstractmethod
    def DescribeClassicLinkInstances(self, params_json_str="{}") -> dict:
        pass

    # ModifyInstanceNetworkSpec	调用ModifyInstanceNetworkSpec修改实例的带宽配置。当实例现有网络规格不满足要求时，可以通过修改实例的带宽配置提高网络性能。
    @abstractmethod
    def ModifyInstanceNetworkSpec(self, params_json_str="{}") -> dict:
        pass
