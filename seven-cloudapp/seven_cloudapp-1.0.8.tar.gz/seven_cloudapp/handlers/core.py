# -*- coding: utf-8 -*-
"""
@Author: HuangJingCan
@Date: 2020-05-26 14:45:44
@LastEditTime: 2020-08-20 17:59:43
@LastEditors: HuangJingCan
@Description: 通用Handler
"""
from seven_cloudapp.handlers.seven_base import *


class IndexHandler(SevenBaseHandler):
    """
    @description: 默认页
    @return: str
    @last_editors: HuangJingCan
    """
    def get_async(self):
        self.write("IndexHandler:" + config.get_value("run_port"))