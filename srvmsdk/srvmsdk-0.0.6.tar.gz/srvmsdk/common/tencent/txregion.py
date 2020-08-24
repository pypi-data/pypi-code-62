#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : txregion.py
# @Author: encircles
# @Date  : 8/19/2020
# @Desc  :
from abc import ABCMeta, abstractmethod


class TxRegion(metaclass=ABCMeta):
    # region 地域相关 ==========================
    @abstractmethod
    def DescribeRegions(self) -> dict:
        pass

    @abstractmethod
    def DescribeZones(self) -> dict:
        pass

    # endregion
