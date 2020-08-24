#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : aliother.py
# @Author: encircles
# @Date  : 8/19/2020
# @Desc  :
from abc import ABCMeta, abstractmethod


class AliOther(metaclass=ABCMeta):
    # 其他接口
    # CancelTask	调用CancelTask取消一件正在运行的任务。目前，您能取消正在运行的导入镜像任务（ImportImage）和导出镜像任务（ExportImage）。
    @abstractmethod
    def CancelTask(self, params_json_str) -> dict:
        pass

    # DescribeTasks	调用DescribeTasks查询一个或多个异步请求的进度。
    @abstractmethod
    def DescribeTasks(self, params_json_str) -> dict:
        pass

    # DescribeTaskAttribute	调用DescribeTaskAttribute查询异步任务的详细信息。目前，可以查询的异步任务有导入镜像（ImportImage）和导出镜像（ExportImage）两种。
    @abstractmethod
    def DescribeTaskAttribute(self, params_json_str) -> dict:
        pass

    # DescribeAccountAttributes	调用DescribeAccountAttributes查询您在一个阿里云地域下能创建的ECS资源配额。包括您能创建的安全组数量、弹性网卡数量、按量付费vCPU核数、抢占式实例vCPU核数、专用宿主机数量、地域网络类型以及账号是否已完成实名认证。
    @abstractmethod
    def DescribeAccountAttributes(self, params_json_str) -> dict:
        pass

    # JoinResourceGroup	调用JoinResourceGroup将一个ECS资源或者服务加入另一个资源组。
    @abstractmethod
    def JoinResourceGroup(self, params_json_str) -> dict:
        pass

    # DescribePrice	（Beta）调用DescribePrice查询云服务器ECS资源的最新价格。
    @abstractmethod
    def DescribePrice(self, params_json_str) -> dict:
        pass

    # DescribeDemands	调用DescribeDemands查询报备资源的交付及使用状态。
    @abstractmethod
    def DescribeDemands(self, params_json_str) -> dict:
        pass
