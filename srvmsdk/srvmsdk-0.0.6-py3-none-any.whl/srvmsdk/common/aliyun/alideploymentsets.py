#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : alideploymentsets.py
# @Author: encircles
# @Date  : 8/19/2020
# @Desc  :
from abc import ABCMeta, abstractmethod


class AliDeploymentSets(metaclass=ABCMeta):
    # 部署集
    # CreateDeploymentSet	调用CreateDeploymentSet在指定的地域内创建一个部署集。
    @abstractmethod
    def CreateDeploymentSet(self, params_json_str) -> dict:
        pass

    # DeleteDeploymentSet	调用DeleteDeploymentSet删除一个部署集。
    @abstractmethod
    def DeleteDeploymentSet(self, params_json_str) -> dict:
        pass

    # ModifyDeploymentSetAttribute	调用ModifyDeploymentSetAttribute修改一个部署集的名称和描述信息。
    @abstractmethod
    def ModifyDeploymentSetAttribute(self, params_json_str) -> dict:
        pass

    # DescribeDeploymentSets	调用DescribeDeploymentSets查询一个或多个部署集的属性列表。
    @abstractmethod
    def DescribeDeploymentSets(self, params_json_str) -> dict:
        pass
