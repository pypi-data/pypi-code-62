#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : alitag.py
# @Author: encircles
# @Date  : 8/19/2020
# @Desc  :
from abc import ABCMeta, abstractmethod


class AliTag(metaclass=ABCMeta):
    # 标签
    # TagResources	调用TagResources为指定的ECS资源列表统一创建并绑定标签。
    @abstractmethod
    def TagResources(self, params_json_str) -> dict:
        pass

    # ListTagResources	调用ListTagResources查询一个或多个ECS资源已经绑定的标签列表。
    @abstractmethod
    def ListTagResources(self, params_json_str) -> dict:
        pass

    # UntagResources	调用UntagResources为指定的ECS资源列表统一解绑并删除标签。
    @abstractmethod
    def UntagResources(self, params_json_str) -> dict:
        pass
