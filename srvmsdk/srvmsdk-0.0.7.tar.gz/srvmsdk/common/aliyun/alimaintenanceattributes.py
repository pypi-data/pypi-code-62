#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : alimaintenanceattributes.py
# @Author: encircles
# @Date  : 8/19/2020
# @Desc  :
from abc import ABCMeta, abstractmethod


class AliMaintenanceAttributes(metaclass=ABCMeta):
    # 运维与监控
    # DescribeDiskMonitorData	调用DescribeDiskMonitorData查询一块云盘指定时间内的使用信息。
    @abstractmethod
    def DescribeDiskMonitorData(self, params_json_str) -> dict:
        pass

    # DescribeInstanceMonitorData	调用DescribeInstanceMonitorData查询一台ECS实例的监控信息。可查询的指标包括ECS实例的vCPU使用率、突发性能实例积分、接收的数据流量、发送的数据流量、平均带宽等。
    @abstractmethod
    def DescribeInstanceMonitorData(self, params_json_str) -> dict:
        pass

    # GetInstanceScreenshot	调用GetInstanceScreenshot获取实例的截屏信息。
    @abstractmethod
    def GetInstanceScreenshot(self, params_json_str) -> dict:
        pass

    # GetInstanceConsoleOutput	调用GetInstanceConsoleOutput获取一台实例的系统命令行输出，数据以Base64编码后返回。
    @abstractmethod
    def GetInstanceConsoleOutput(self, params_json_str) -> dict:
        pass

    # DescribeEniMonitorData	调用DescribeEniMonitorData查询一块辅助网卡在指定时间段内使用的流量信息。
    @abstractmethod
    def DescribeEniMonitorData(self, params_json_str) -> dict:
        pass

    # RedeployInstance	当ECS实例收到系统事件通知时，调用RedeployInstance可以重新部署这台ECS实例。
    @abstractmethod
    def RedeployInstance(self, params_json_str) -> dict:
        pass

    # DescribeSnapshotMonitorData	调用DescribeSnapshotMonitorData查询一个地域下近30天内的快照容量变化监控数据。
    @abstractmethod
    def DescribeSnapshotMonitorData(self, params_json_str) -> dict:
        pass

    # DescribeInstanceMaintenanceAttributes	调用DescribeInstanceMaintenanceAttributes查询实例的维护属性。
    @abstractmethod
    def DescribeInstanceMaintenanceAttributes(self, params_json_str) -> dict:
        pass

    # ModifyInstanceMaintenanceAttributes	调用ModifyInstanceMaintenanceAttributes修改实例的维护属性。
    @abstractmethod
    def ModifyInstanceMaintenanceAttributes(self, params_json_str) -> dict:
        pass
