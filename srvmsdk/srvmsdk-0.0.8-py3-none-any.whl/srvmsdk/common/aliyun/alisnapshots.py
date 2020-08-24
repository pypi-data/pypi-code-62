#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : alisnapshots.py
# @Author: encircles
# @Date  : 8/19/2020
# @Desc  :
from abc import ABCMeta, abstractmethod


class AliSnapshots(metaclass=ABCMeta):
    # 快照
    # CreateSnapshot	调用CreateSnapshot为一块云盘创建一份快照。
    @abstractmethod
    def CreateSnapshot(self, params_json_str="{}") -> dict:
        pass

    # CreateAutoSnapshotPolicy	调用CreateAutoSnapshotPolicy创建一条自动快照策略。
    @abstractmethod
    def CreateAutoSnapshotPolicy(self, params_json_str="{}") -> dict:
        pass

    # ApplyAutoSnapshotPolicy	调用ApplyAutoSnapshotPolicy为一块或者多块云盘应用自动快照策略。目标云盘已经应用了自动快照策略时，调用ApplyAutoSnapshotPolicy可以更换云盘当前应用的自动快照策略。
    @abstractmethod
    def ApplyAutoSnapshotPolicy(self, params_json_str="{}") -> dict:
        pass

    # CopySnapshot	调用CopySnapshot将一份普通快照从一个地域复制到另一个地域。
    @abstractmethod
    def CopySnapshot(self, params_json_str="{}") -> dict:
        pass

    # DeleteSnapshot	调用DeleteSnapshot删除指定的快照。如果需要取消正在创建的快照，也可以调用该接口删除快照，即取消创建快照任务。
    @abstractmethod
    def DeleteSnapshot(self, params_json_str="{}") -> dict:
        pass

    # CancelAutoSnapshotPolicy	调用CancelAutoSnapshotPolicy取消一块或者多块云盘的自动快照策略。
    @abstractmethod
    def CancelAutoSnapshotPolicy(self, params_json_str="{}") -> dict:
        pass

    # DeleteAutoSnapshotPolicy	删除一条自动快照策略。如果目标自动快照策略已经被应用到磁盘上，删除自动快照策略后，这些磁盘不再执行该策略。
    @abstractmethod
    def DeleteAutoSnapshotPolicy(self, params_json_str="{}") -> dict:
        pass

    # DescribeAutoSnapshotPolicyEX	调用DescribeAutoSnapshotPolicyEX查询您已创建的自动快照策略。
    @abstractmethod
    def DescribeAutoSnapshotPolicyEX(self, params_json_str="{}") -> dict:
        pass

    # DescribeSnapshots	调用DescribeSnapshots查询一台ECS实例或一块云盘所有的快照列表。InstanceId、DiskId和SnapshotIds不是必需参数，但是可以构建过滤器逻辑，参数之间为逻辑与（And）关系。
    @abstractmethod
    def DescribeSnapshots(self, params_json_str="{}") -> dict:
        pass

    # DescribeSnapshotLinks	调用DescribeSnapshotLinks查询云盘快照链。快照链是一块云盘所有快照组成的关系链，一块云盘对应一条快照链。
    @abstractmethod
    def DescribeSnapshotLinks(self, params_json_str="{}") -> dict:
        pass

    # ModifyAutoSnapshotPolicyEx	调用ModifyAutoSnapshotPolicyEx修改一条自动快照策略。修改自动快照策略后，之前已应用该策略的云盘随即执行修改后的自动快照策略。
    @abstractmethod
    def ModifyAutoSnapshotPolicyEx(self, params_json_str="{}") -> dict:
        pass

    # DescribeSnapshotsUsage	调用DescribeSnapshotsUsage查询您在一个地域下的快照数量以及快照容量。
    @abstractmethod
    def DescribeSnapshotsUsage(self, params_json_str="{}") -> dict:
        pass

    # DescribeSnapshotPackage	调用DescribeSnapshotPackage查询您在一个阿里云地域下已经购买的对象存储OSS存储包，存储包可以用于抵扣快照存储容量。
    @abstractmethod
    def DescribeSnapshotPackage(self, params_json_str="{}") -> dict:
        pass

    # ModifySnapshotAttribute	调用ModifySnapshotAttribute修改一份快照的名称或描述。
    @abstractmethod
    def ModifySnapshotAttribute(self, params_json_str="{}") -> dict:
        pass
