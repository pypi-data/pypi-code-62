#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : tximages.py
# @Author: encircles
# @Date  : 8/19/2020
# @Desc  :
from abc import ABCMeta, abstractmethod


class TxImages(metaclass=ABCMeta):
    # region 镜像相关接口 ==========================
    # CreateImage	创建镜像
    @abstractmethod
    def CreateImage(self, params_json_str) -> dict:
        pass

    # DeleteImages	删除镜像
    @abstractmethod
    def DeleteImages(self, params_json_str) -> dict:
        pass

    # ModifyImageAttribute	修改镜像属性
    @abstractmethod
    def ModifyImageAttribute(self, params_json_str) -> dict:
        pass

    # DescribeImages	查看镜像列表
    @abstractmethod
    def DescribeImages(self, params_json_str) -> dict:
        pass

    # ImportImage	外部镜像导入
    @abstractmethod
    def ImportImage(self, params_json_str) -> dict:
        pass

    # DescribeImportImageOs	查询外部导入镜像支持的OS列表
    @abstractmethod
    def DescribeImportImageOs(self, params_json_str) -> dict:
        pass

    # DescribeImageSharePermission	查看镜像分享信息
    @abstractmethod
    def DescribeImageSharePermission(self, params_json_str) -> dict:
        pass

    # ModifyImageSharePermission	修改镜像分享信息
    @abstractmethod
    def ModifyImageSharePermission(self, params_json_str) -> dict:
        pass

    # SyncImages	同步镜像
    @abstractmethod
    def SyncImages(self, params_json_str) -> dict:
        pass

    # DescribeImageQuota	查询镜像配额上限
    @abstractmethod
    def DescribeImageQuota(self, params_json_str) -> dict:
        pass
    # endregion
