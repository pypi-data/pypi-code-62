#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : client.py
# @Author: encircles
# @Date  : 8/19/2020
# @Desc  :
from srvmsdk.common.aliyun.alibase import AliCommonBase


class AliClient(AliCommonBase):
    def DescribeRegions(self):
        pass

    def DescribeZones(self):
        pass

    def RunInstances(self, params_json_str):
        pass

    def InquiryPriceRunInstances(self, params_json_str):
        pass
