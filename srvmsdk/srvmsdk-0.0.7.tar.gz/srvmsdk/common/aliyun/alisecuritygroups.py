#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : alisecuritygroups.py
# @Author: encircles
# @Date  : 8/19/2020
# @Desc  :
from abc import ABCMeta, abstractmethod


class AliSecurityGroups(metaclass=ABCMeta):
    # 安全组
    # CreateSecurityGroup	调用CreateSecurityGroup新建一个安全组。新建的安全组，默认只允许安全组内的实例互相访问，安全组外的一切通信请求会被拒绝。若您想允许其他安全组实例的通信请求，或者来自互联网的访问请求，需要授权安全组权限（AuthorizeSecurityGroup）。
    @abstractmethod
    def CreateSecurityGroup(self, params_json_str) -> dict:
        pass

    # AuthorizeSecurityGroup	调用AuthorizeSecurityGroup增加一条安全组入方向规则。指定安全组入方向的访问权限，允许或者拒绝其他设备发送入方向流量到安全组里的实例。
    @abstractmethod
    def AuthorizeSecurityGroup(self, params_json_str) -> dict:
        pass

    # AuthorizeSecurityGroupEgress	调用AuthorizeSecurityGroupEgress增加一条安全组出方向规则。指定安全组出方向的访问权限，允许或者拒绝安全组里的实例发送出方向流量到其他设备。
    @abstractmethod
    def AuthorizeSecurityGroupEgress(self, params_json_str) -> dict:
        pass

    # RevokeSecurityGroup	调用RevokeSecurityGroup删除一条安全组入方向规则，撤销安全组入方向的权限设置。
    @abstractmethod
    def RevokeSecurityGroup(self, params_json_str) -> dict:
        pass

    # RevokeSecurityGroupEgress	调用RevokeSecurityGroupEgress删除一条安全组出方向规则，撤销安全组出方向的访问权限。
    @abstractmethod
    def RevokeSecurityGroupEgress(self, params_json_str) -> dict:
        pass

    # JoinSecurityGroup	调用JoinSecurityGroup将一台ECS实例加入到指定的安全组。
    @abstractmethod
    def JoinSecurityGroup(self, params_json_str) -> dict:
        pass

    # LeaveSecurityGroup	调用LeaveSecurityGroup将一台ECS实例移出指定的安全组。
    @abstractmethod
    def LeaveSecurityGroup(self, params_json_str) -> dict:
        pass

    # DeleteSecurityGroup	调用DeleteSecurityGroup删除一个安全组。
    @abstractmethod
    def DeleteSecurityGroup(self, params_json_str) -> dict:
        pass

    # DescribeSecurityGroupAttribute	调用DescribeSecurityGroupAttribute查询一个安全组的安全组规则。
    @abstractmethod
    def DescribeSecurityGroupAttribute(self, params_json_str) -> dict:
        pass

    # DescribeSecurityGroups	调用DescribeSecurityGroups查询您创建的安全组的基本信息，例如安全组ID和安全组描述等。返回列表按照安全组ID降序排列。
    @abstractmethod
    def DescribeSecurityGroups(self, params_json_str) -> dict:
        pass

    # DescribeSecurityGroupReferences	调用DescribeSecurityGroupReferences查询一个安全组和其他哪些安全组有安全组级别的授权行为。
    @abstractmethod
    def DescribeSecurityGroupReferences(self, params_json_str) -> dict:
        pass

    # ModifySecurityGroupAttribute	调用ModifySecurityGroupAttribute修改指定安全组的属性，包括修改安全组名称和描述。
    @abstractmethod
    def ModifySecurityGroupAttribute(self, params_json_str) -> dict:
        pass

    # ModifySecurityGroupPolicy	调用ModifySecurityGroupPolicy修改安全组内网连通策略。
    @abstractmethod
    def ModifySecurityGroupPolicy(self, params_json_str) -> dict:
        pass

    # ModifySecurityGroupRule	调用ModifySecurityGroupRule修改安全组入方向规则的描述信息。如果您还没有增加过安全组规则，可以调用AuthorizeSecurityGroup增加。
    @abstractmethod
    def ModifySecurityGroupRule(self, params_json_str) -> dict:
        pass

    # ModifySecurityGroupEgressRule	调用ModifySecurityGroupEgressRule修改安全组出方向规则的描述信息。如果您还没有增加过安全组规则，可以调用AuthorizeSecurityGroupEgress增加。
    @abstractmethod
    def ModifySecurityGroupEgressRule(self, params_json_str) -> dict:
        pass
