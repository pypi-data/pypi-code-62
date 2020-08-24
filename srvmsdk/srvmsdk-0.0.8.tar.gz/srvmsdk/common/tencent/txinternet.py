#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : txinternet.py
# @Author: encircles
# @Date  : 8/19/2020
# @Desc  :
from abc import ABCMeta, abstractmethod


class TxInternet(metaclass=ABCMeta):

    # region 网络相关接口
    # DescribeInstanceInternetBandwidthConfigs	查询实例带宽配置
    @abstractmethod
    def DescribeInstanceInternetBandwidthConfigs(self, params_json_str="{}") -> dict:
        pass

    # DescribeInternetChargeTypeConfigs	查询网络计费类型
    @abstractmethod
    def DescribeInternetChargeTypeConfigs(self, params_json_str="{}") -> dict:
        pass

    # InquiryPriceResetInstancesInternetMaxBandwidth	调整实例带宽上限询价
    @abstractmethod
    def InquiryPriceResetInstancesInternetMaxBandwidth(self, params_json_str="{}") -> dict:
        pass

    # ModifyInstancesVpcAttribute	修改实例vpc属性
    @abstractmethod
    def ModifyInstancesVpcAttribute(self, params_json_str="{}") -> dict:
        pass

    # ResetInstancesInternetMaxBandwidth	调整实例带宽上限
    @abstractmethod
    def ResetInstancesInternetMaxBandwidth(self, params_json_str="{}") -> dict:
        pass
    # endregion
