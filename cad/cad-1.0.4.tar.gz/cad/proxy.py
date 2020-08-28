#!/usr/bin/env python
# -*- coding:utf-8 _*-
"""
@license : Copyright(C), WAYZ
@author  : Bruce Liu
@time    : 2020/7/17
@contact : bruce.liu@wayz.ai
"""
from functools import wraps

from dynaconf import settings as ds

from cad.app_config_util import AppConfigUtil, CadException


class ProxyException(BaseException):
    def __init__(self, msg: str):
        self._msg = msg

    def __str__(self):
        return self._msg


def base_error_response(msg):
    """
    默认异常处理函数，抛出ProxyException异常
    :param msg:
    :return:
    """
    raise ProxyException(msg)


def cad_proxy(auth_code: str, error_response=base_error_response):
    """
    鉴权修饰器
    :param auth_code: 权限code
    :param error_response: 返回异常结果的函数，要求：接受一个字符串类型的入参,用于说明异常原因，可以返回对应框架的response对象或抛出异常
    :return:
    """

    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            try:
                # 获取应用ak
                ak = args[1].headers.get('authorization').split(':')[1]
                # 根据应用ak及权限code判断是否拥有对应权限
                if AppConfigUtil(int(ds.APP_ID)).check(ak=ak, sk=None, auth_code=auth_code):
                    return func(*args, **kwargs)
                else:
                    # 如果没有权限返回with False
                    return error_response('Invalid authorization, with detail False')
            except CadException:
                # 如果ak不存在，返回CadException
                return error_response('Invalid authorization, with CadException')

        return inner

    return wrapper
