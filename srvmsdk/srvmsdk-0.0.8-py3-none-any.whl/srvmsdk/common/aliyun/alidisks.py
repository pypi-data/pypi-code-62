#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : alidisks.py
# @Author: encircles
# @Date  : 8/19/2020
# @Desc  :
from abc import ABCMeta, abstractmethod


class AliDisks(metaclass=ABCMeta):
    # 块存储
    # CreateDisk	调用CreateDisk创建一块按量付费或包年包月数据盘。云盘类型包括普通云盘、高效云盘、SSD云盘和ESSD云盘。
    @abstractmethod
    def CreateDisk(self, params_json_str="{}") -> dict:
        pass

    # DeleteDisk	调用DeleteDisk释放一块按量付费数据盘。磁盘类型包括普通云盘、高效云盘、SSD云盘和ESSD云盘。
    @abstractmethod
    def DeleteDisk(self, params_json_str="{}") -> dict:
        pass

    # DescribeDisks	调用DescribeDisks查询一块或多块您已经创建的云盘以及本地盘。
    @abstractmethod
    def DescribeDisks(self, params_json_str="{}") -> dict:
        pass

    # AttachDisk	调用AttachDisk为一台ECS实例挂载一块按量付费数据盘。
    @abstractmethod
    def AttachDisk(self, params_json_str="{}") -> dict:
        pass

    # DetachDisk	调用DetachDisk从一台实例上卸载一块按量付费磁盘。磁盘类型包括普通云盘、高效云盘和SSD云盘。
    @abstractmethod
    def DetachDisk(self, params_json_str="{}") -> dict:
        pass

    # ModifyDiskAttribute	调用ModifyDiskAttribute修改您的磁盘的属性或者明细。
    @abstractmethod
    def ModifyDiskAttribute(self, params_json_str="{}") -> dict:
        pass

    # ReplaceSystemDisk	调用ReplaceSystemDisk更换一台ECS实例的系统盘或者操作系统。
    @abstractmethod
    def ReplaceSystemDisk(self, params_json_str="{}") -> dict:
        pass

    # ReInitDisk	调用ReInitDisk重新初始化一块云盘到创建时的初始状态。
    @abstractmethod
    def ReInitDisk(self, params_json_str="{}") -> dict:
        pass

    # ResetDisk	调用ResetDisk使用磁盘的历史快照回滚至某一阶段的磁盘状态。
    @abstractmethod
    def ResetDisk(self, params_json_str="{}") -> dict:
        pass

    # ResizeDisk	调用ResizeDisk扩容一块云盘，支持扩容系统盘和数据盘。
    @abstractmethod
    def ResizeDisk(self, params_json_str="{}") -> dict:
        pass

    # ModifyDiskChargeType	调用ModifyDiskChargeType修改一台实例上挂载的一块或最多16块云盘的计费方式。
    @abstractmethod
    def ModifyDiskChargeType(self, params_json_str="{}") -> dict:
        pass

    # ModifyDiskSpec	调用ModifyDiskSpec升级一块ESSD云盘的性能等级。
    @abstractmethod
    def ModifyDiskSpec(self, params_json_str="{}") -> dict:
        pass
