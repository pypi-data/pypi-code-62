#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : txsecuritygroups.py
# @Author: encircles
# @Date  : 8/19/2020
# @Desc  :
from abc import ABCMeta, abstractmethod


class TxSecurityGroups(metaclass=ABCMeta):
    # region 安全组相关接口
    # AssociateSecurityGroups 绑定安全组
    @abstractmethod
    def AssociateSecurityGroups(self, params_json_str="{}") -> dict:
        pass

    # DisassociateSecurityGroups 解绑安全组
    @abstractmethod
    def DisassociateSecurityGroups(self, params_json_str="{}") -> dict:
        pass
    # endregion
