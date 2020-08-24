#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : alitemplates.py
# @Author: encircles
# @Date  : 8/19/2020
# @Desc  :
from abc import ABCMeta, abstractmethod


class AliTemplates(metaclass=ABCMeta):
    # 启动模板
    # CreateLaunchTemplate	调用CreateLaunchTemplate创建一个实例启动模板，简称模板。实例启动模板能免除您每次创建实例时都需要填入大量配置参数。
    @abstractmethod
    def CreateLaunchTemplate(self, params_json_str="{}") -> dict:
        pass

    # CreateLaunchTemplateVersion	调用CreateLaunchTemplateVersion根据指定的实例启动模板创建一个版本。
    @abstractmethod
    def CreateLaunchTemplateVersion(self, params_json_str="{}") -> dict:
        pass

    # DeleteLaunchTemplate	调用DeleteLaunchTemplate删除一个实例启动模板。
    @abstractmethod
    def DeleteLaunchTemplate(self, params_json_str="{}") -> dict:
        pass

    # DeleteLaunchTemplateVersion	调用DeleteLaunchTemplateVersion删除指定实例启动模板的一个版本。不支持删除默认版本，您需要通过DeleteLaunchTemplate删除整个实例启动模板才能删除默认版本。
    @abstractmethod
    def DeleteLaunchTemplateVersion(self, params_json_str="{}") -> dict:
        pass

    # DescribeLaunchTemplates	调用DescribeLaunchTemplates查询一个或多个可用的实例启动模板。
    @abstractmethod
    def DescribeLaunchTemplates(self, params_json_str="{}") -> dict:
        pass

    # DescribeLaunchTemplateVersions	调用DescribeLaunchTemplateVersions查询实例启动模板版本。
    @abstractmethod
    def DescribeLaunchTemplateVersions(self, params_json_str="{}") -> dict:
        pass

    # ModifyLaunchTemplateDefaultVersion	调用ModifyLaunchTemplateDefaultVersion切换启动模板的某个版本为该模板的默认版本。如果您在创建实例（RunInstances）时不指定模板版本号，会采用默认版本。
    @abstractmethod
    def ModifyLaunchTemplateDefaultVersion(self, params_json_str="{}") -> dict:
        pass
