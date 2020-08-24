#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : utils.py
# @Author: encircles
# @Date  : 8/18/2020
# @Desc  :
import json

from srvmsdk.common import errcode


def ret_msg(code=errcode.SUCCESS, msg=None, result=None) -> dict:
    """
    返回官方结果数据
    :param code: 200为成功, 其他为失败
    :param msg: 信息
    :param result: 传入json字符串
    :return: dictS
    """
    if result is not None:
        try:
            result = json.loads(result)
        except ValueError:
            result = None

    return {
        "code": code,
        "msg": msg,
        "result": result
    }


def hello_world():
    pass
