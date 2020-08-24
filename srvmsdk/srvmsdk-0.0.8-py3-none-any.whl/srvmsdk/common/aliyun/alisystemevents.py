#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : alisystemevents.py
# @Author: encircles
# @Date  : 8/19/2020
# @Desc  :
from abc import ABCMeta, abstractmethod


class AliSystemEvents(metaclass=ABCMeta):
    # 系统事件
    # DescribeDisksFullStatus	调用DescribeDisksFullStatus查询一块或多块块存储的全部状态信息。
    @abstractmethod
    def DescribeDisksFullStatus(self, params_json_str="{}") -> dict:
        pass

    # DescribeInstancesFullStatus	调用DescribeInstancesFullStatus查询一台或多台实例的全状态信息。全状态信息包括实例状态和实例系统事件状态，其中，实例状态为实例的生命周期状态，实例系统事件为维护事件的健康状态。
    @abstractmethod
    def DescribeInstancesFullStatus(self, params_json_str="{}") -> dict:
        pass

    # DescribeInstanceHistoryEvents	调用DescribeInstanceHistoryEvents查询指定实例的系统事件信息，默认查询处于非活跃状态的历史系统事件。
    @abstractmethod
    def DescribeInstanceHistoryEvents(self, params_json_str="{}") -> dict:
        pass

    # CancelSimulatedSystemEvents	调用CancelSimulatedSystemEvents取消一件或多件处于Scheduled（计划中）或Executing（执行中）状态的模拟系统事件。取消系统事件后，模拟事件变为Canceled（已取消）状态。
    @abstractmethod
    def CancelSimulatedSystemEvents(self, params_json_str="{}") -> dict:
        pass

    # CreateSimulatedSystemEvents	调用CreateSimulatedSystemEvents为一台或多台ECS实例预约模拟系统事件。模拟系统事件相当于事件演习，不会真正执行事件，也不会对ECS实例产生影响。
    @abstractmethod
    def CreateSimulatedSystemEvents(self, params_json_str="{}") -> dict:
        pass

    # AcceptInquiredSystemEvent	调用AcceptInquiredSystemEvent接受并授权执行系统事件操作。对问询中（Inquiring）状态的系统事件，接受系统事件的默认操作，授权系统执行默认操作。
    @abstractmethod
    def AcceptInquiredSystemEvent(self, params_json_str="{}") -> dict:
        pass
