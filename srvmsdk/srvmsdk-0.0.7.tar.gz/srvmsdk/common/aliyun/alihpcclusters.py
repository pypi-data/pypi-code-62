#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : alihpcclusters.py
# @Author: encircles
# @Date  : 8/19/2020
# @Desc  :
from abc import ABCMeta, abstractmethod


class AliHpcClusters(metaclass=ABCMeta):
    # 高性能集群
    # DeleteHpcCluster	调用DeleteHpcCluster删除一个HPC集群。
    @abstractmethod
    def DeleteHpcCluster(self, params_json_str) -> dict:
        pass

    # CreateHpcCluster	调用CreateHpcCluster创建一个HPC集群。
    @abstractmethod
    def CreateHpcCluster(self, params_json_str) -> dict:
        pass

    # DescribeHpcClusters	调用DescribeHpcClusters查询您可用的HPC集群。请求参数作为筛选器（Filter）使用，筛选关系为逻辑与（&&）关系，参数之间无依赖关系。
    @abstractmethod
    def DescribeHpcClusters(self, params_json_str) -> dict:
        pass

    # ModifyHpcClusterAttribute	调用ModifyHpcClusterAttribute修改一个HPC集群的描述信息。
    @abstractmethod
    def ModifyHpcClusterAttribute(self, params_json_str) -> dict:
        pass
