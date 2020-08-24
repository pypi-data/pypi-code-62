#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : aliregion.py
# @Author: encircles
# @Date  : 8/19/2020
# @Desc  :
from abc import ABCMeta, abstractmethod


class AliRegion(metaclass=ABCMeta):

    # region 地域
    # DescribeRegions	调用DescribeRegions查询您可以使用的阿里云地域。
    @abstractmethod
    def DescribeRegions(self) -> dict:
        pass

    # DescribeZones	调用DescribeZones查询一个阿里云地域下的可用区。
    @abstractmethod
    def DescribeZones(self) -> dict:
        pass

    # DescribeAvailableResource	调用DescribeAvailableResource查询某一可用区的资源列表。例如，您可以在某一可用区创建实例（RunInstances
    # ）或者修改实例规格（ModifyInstanceSpec）时查询该可用区的资源列表。
    @abstractmethod
    def DescribeAvailableResource(self, params_json_str="{}") -> dict:
        pass

    # DescribeResourcesModification	调用DescribeResourcesModification查询升级和降配实例规格或者系统盘时，某一可用区的可用资源信息。
    @abstractmethod
    def DescribeResourcesModification(self, params_json_str="{}") -> dict:
        pass
    # endregion
