#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : aliimages.py
# @Author: encircles
# @Date  : 8/19/2020
# @Desc  :
from abc import ABCMeta, abstractmethod


class AliImages(metaclass=ABCMeta):
    # 镜像
    # CreateImage	调用CreateImage创建一份自定义镜像。您可以使用创建的自定义镜像创建ECS实例（RunInstances）或者更换实例的系统盘（ReplaceSystemDisk）。
    @abstractmethod
    def CreateImage(self, params_json_str) -> dict:
        pass

    # ImportImage	调用ImportImage导入您已有的镜像文件到云服务器ECS，并作为自定义镜像出现在相应地域中。
    @abstractmethod
    def ImportImage(self, params_json_str) -> dict:
        pass

    # ExportImage	调用ExportImage导出您的自定义镜像到与该自定义镜像同一地域的OSS Bucket里。
    @abstractmethod
    def ExportImage(self, params_json_str) -> dict:
        pass

    # CopyImage	调用CopyImage复制一个地域下的自定义镜像到其他地域。复制镜像可以实现跨地域部署ECS实例、跨地域复制ECS实例等目的。
    @abstractmethod
    def CopyImage(self, params_json_str) -> dict:
        pass

    # CancelCopyImage	调用CancelCopyImage取消正在进行中的复制镜像（CopyImage）任务。
    @abstractmethod
    def CancelCopyImage(self, params_json_str) -> dict:
        pass

    # DescribeImages	调用DescribeImages查询您可以使用的镜像资源。
    @abstractmethod
    def DescribeImages(self, params_json_str) -> dict:
        pass

    # DeleteImage	调用DeleteImage删除一份自定义镜像。
    @abstractmethod
    def DeleteImage(self, params_json_str) -> dict:
        pass

    # DescribeImageSharePermission	调用DescribeImageSharePermission查询一份自定义镜像已经共享的所有用户。返回结果支持分页显示，每页的信息条目默认为10条。
    @abstractmethod
    def DescribeImageSharePermission(self, params_json_str) -> dict:
        pass

    # ModifyImageAttribute	调用ModifyImageAttribute修改一份自定义镜像的名称或描述信息。
    @abstractmethod
    def ModifyImageAttribute(self, params_json_str) -> dict:
        pass

    # ModifyImageSharePermission	调用ModifyImageSharePermission管理镜像共享权限。您可以将自己的自定义镜像共享给其他阿里云用户，该用户可以使用共享的自定义镜像创建ECS实例（RunInstances）或者更换实例的系统盘（ReplaceSystemDisk）。
    @abstractmethod
    def ModifyImageSharePermission(self, params_json_str) -> dict:
        pass

    # DescribeImageSupportInstanceTypes	调用DescribeImageSupportInstanceTypes查询指定镜像支持的实例规格。
    @abstractmethod
    def DescribeImageSupportInstanceTypes(self, params_json_str) -> dict:
        pass
