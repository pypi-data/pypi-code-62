#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : alinetworkinterface.py
# @Author: encircles
# @Date  : 8/19/2020
# @Desc  :
from abc import ABCMeta, abstractmethod


class AliNetworkInterfaces(metaclass=ABCMeta):
    # 弹性网卡
    # CreateNetworkInterface	调用CreateNetworkInterface创建一个弹性网卡（ENI）。
    @abstractmethod
    def CreateNetworkInterface(self, params_json_str) -> dict:
        pass

    # AttachNetworkInterface	调用AttachNetworkInterface附加弹性网卡（ENI）到专有网络（VPC）类型实例上。
    @abstractmethod
    def AttachNetworkInterface(self, params_json_str) -> dict:
        pass

    # DetachNetworkInterface	调用DetachNetworkInterface从一台实例上分离一个弹性网卡（ENI）。
    @abstractmethod
    def DetachNetworkInterface(self, params_json_str) -> dict:
        pass

    # DeleteNetworkInterface	调用DeleteNetworkInterface删除一个弹性网卡（ENI）。
    @abstractmethod
    def DeleteNetworkInterface(self, params_json_str) -> dict:
        pass

    # DescribeNetworkInterfaces	调用DescribeNetworkInterfaces查看弹性网卡（ENI）列表。
    @abstractmethod
    def DescribeNetworkInterfaces(self, params_json_str) -> dict:
        pass

    # ModifyNetworkInterfaceAttribute	调用ModifyNetworkInterfaceAttribute修改一个弹性网卡（ENI）的属性。例如，弹性网卡名称、描述以及所属安全组等。
    @abstractmethod
    def ModifyNetworkInterfaceAttribute(self, params_json_str) -> dict:
        pass

    # AssignPrivateIpAddresses	调用AssignPrivateIpAddresses为一块弹性网卡分配一个或多个辅助私有IP地址。可以为网卡指定在所属虚拟交换机（VSwitch）的CIDR私有IP地址，或者通过指定私有网络地址数量自动创建私有IP地址。
    @abstractmethod
    def AssignPrivateIpAddresses(self, params_json_str) -> dict:
        pass

    # UnassignPrivateIpAddresses	调用UnassignPrivateIpAddresses从一块弹性网卡删除一个或多个辅助私有IP地址。
    @abstractmethod
    def UnassignPrivateIpAddresses(self, params_json_str) -> dict:
        pass

    # AssignIpv6Addresses	调用AssignIpv6Addresses为弹性网卡分配一个或多个IPv6地址。
    @abstractmethod
    def AssignIpv6Addresses(self, params_json_str) -> dict:
        pass

    # UnassignIpv6Addresses	若弹性网卡已被分配了IPv6地址，调用UnassignIpv6Addresses可以回收一个或多个IPv6地址。
    @abstractmethod
    def UnassignIpv6Addresses(self, params_json_str) -> dict:
        pass
