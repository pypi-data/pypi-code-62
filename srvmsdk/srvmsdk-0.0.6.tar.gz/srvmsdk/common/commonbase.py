#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : alibase.py
# @Author: encircles
# @Date  : 8/19/2020
# @Desc  :
from abc import ABCMeta

from srvmsdk.common.instances import InstancesABC
from srvmsdk.common.region import RegionABC


class CommonBase(InstancesABC, RegionABC, metaclass=ABCMeta):
    pass
