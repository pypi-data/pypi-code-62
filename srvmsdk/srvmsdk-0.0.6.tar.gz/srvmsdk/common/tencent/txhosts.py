#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : txhosts.py
# @Author: encircles
# @Date  : 8/19/2020
# @Desc  :
from abc import ABCMeta, abstractmethod


class TxHosts(metaclass=ABCMeta):

    # region 专用宿主机相关接口
    # AllocateHosts	创建CDH实例
    @abstractmethod
    def AllocateHosts(self, params_json_str) -> dict:
        pass

    # DescribeHosts	查看CDH实例列表
    @abstractmethod
    def DescribeHosts(self, params_json_str) -> dict:
        pass

    # ModifyHostsAttribute	修改CDH实例的属性
    @abstractmethod
    def ModifyHostsAttribute(self, params_json_str) -> dict:
        pass

    # RenewHosts	续费CDH实例
    @abstractmethod
    def RenewHosts(self, params_json_str) -> dict:
        pass

    # endregion
