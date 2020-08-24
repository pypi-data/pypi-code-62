#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : alicloudassistant.py
# @Author: encircles
# @Date  : 8/19/2020
# @Desc  :
from abc import ABCMeta, abstractmethod


class AliCloudAssistant(metaclass=ABCMeta):
    # 云助手
    # CreateCommand	调用CreateCommand新建一条云助手命令。
    @abstractmethod
    def CreateCommand(self, params_json_str="{}") -> dict:
        pass

    # InvokeCommand	调用InvokeCommand为一台或多台ECS实例触发一条云助手命令。
    @abstractmethod
    def InvokeCommand(self, params_json_str="{}") -> dict:
        pass

    # StopInvocation	调用StopInvocation停止一台或多台ECS实例中一条正在进行中（Running）的云助手命令进程。
    @abstractmethod
    def StopInvocation(self, params_json_str="{}") -> dict:
        pass

    # DeleteCommand	调用DeleteCommand删除一条云助手命令。
    @abstractmethod
    def DeleteCommand(self, params_json_str="{}") -> dict:
        pass

    # DescribeCommands	调用DescribeCommands查询您已经创建的云助手命令。只输入参数Action和RegionId，不输入其他任何请求参数，则默认查询您所有可用的命令（CommandId）。
    @abstractmethod
    def DescribeCommands(self, params_json_str="{}") -> dict:
        pass

    # DescribeInvocations	调用DescribeInvocations查询最近两周云助手脚本的执行列表和状态。
    @abstractmethod
    def DescribeInvocations(self, params_json_str="{}") -> dict:
        pass

    # DescribeInvocationResults	调用DescribeInvocationResults查看云助手命令的执行结果，在指定ECS实例中的实际执行结果。
    @abstractmethod
    def DescribeInvocationResults(self, params_json_str="{}") -> dict:
        pass

    # DescribeCloudAssistantStatus	调用DescribeCloudAssistantStatus查询一台或者多台实例是否安装了云助手客户端。
    @abstractmethod
    def DescribeCloudAssistantStatus(self, params_json_str="{}") -> dict:
        pass

    # InstallCloudAssistant	调用InstallCloudAssistant为一台或多台实例安装云助手客户端。
    @abstractmethod
    def InstallCloudAssistant(self, params_json_str="{}") -> dict:
        pass

    # RunCommand	调用RunCommand新建一份Shell、PowerShell或者Bat类型的云助手脚本，然后在一台或多台ECS实例中执行该脚本。
    @abstractmethod
    def RunCommand(self, params_json_str="{}") -> dict:
        pass
