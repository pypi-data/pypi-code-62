#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Date   : 2020/8/18
# @Author : Bruce Liu /Lin Luo
# @Mail   : 15869300264@163.com
import socket
from datetime import datetime
from functools import wraps
from json import dumps

from dynaconf import settings as dynasettings

from cad import __version__ as version
from .exceptions import CadException
from .redis_util import RedisUtil


def get_ip():
    """
    获取ip
    :return:
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


ip = get_ip()


def basic_info() -> dict:
    """
    获取日志基础信息
    :return:
    """
    hostname = socket.gethostname()
    return {'hostname': hostname, 'ip': ip, 'time': str(datetime.now()), 'version': version}


class LogUtil(object):
    """
    日志记录修饰器类
    """

    def __init__(self, redis_url_str: str = None):
        if redis_url_str is None:
            redis_url_str = dynasettings.REDIS_ADDRESS
        self._log_key = f'{dynasettings.APPLICATION_NAME}:log'
        self._redis_client = RedisUtil(url_str=redis_url_str).redis

    def __call__(self, func):
        """
        call方法，处理实现修饰器逻辑
        :param func:
        :return:
        """

        @wraps(func)
        def inner(func_self, *args, **kwargs):
            try:
                res = func(func_self, *args, **kwargs)
                if not getattr(func_self, '_is_log', True):
                    return res
                # 根据不同的函数，执行不同的处理方法
                if func.__name__ == 'check':
                    items = self._app_config_util_check(func_self, *args, **kwargs)
                    items['res'] = res
                elif func.__name__ == 'get_sk':
                    items = self._app_config_util_get_sk(func_self, *args, **kwargs)
                elif func.__name__ == 'get':
                    items = self._cad_util_get(func_self, *args, *kwargs)
                else:
                    items = basic_info()
                    items['error'] = 'unknown function'
                items['method'] = func.__qualname__
                self._add_log(dumps(items))
            except CadException as e:
                # 只处理CadException异常
                items = basic_info()
                items['error'] = f'CadException: {str(e)}'
                self._add_log(dumps(items))
                # 处理完CadException后，继续将原来的异常抛出
                raise e
            return res

        return inner

    def _add_log(self, info: str) -> None:
        """
        向列表中添加日志
        :param info:
        :return:
        """
        self._redis_client.rpush(self._log_key, info)

    @staticmethod
    def _cad_util_get(self, ak) -> dict:
        """
        处理CadUtil的get方法
        :param self:
        :param ak:
        :return:
        """
        items = basic_info()
        items['ak'] = ak
        return items

    @staticmethod
    def _app_config_util_get_sk(self, ak, dict_obj: dict = None) -> dict:
        """
        处理AppConfigUtil的get_sk方法
        :param self:
        :param ak:
        :param dict_obj:
        :return:
        """
        items = basic_info()
        items['app_id'] = self._app_id
        items['ak'] = ak
        items['dict_obj'] = dict_obj
        return items

    @staticmethod
    def _app_config_util_check(self, ak: str, sk: str or None, auth_code: str = None,
                               dict_obj: dict = None) -> dict:
        """
        处理AppConfigUtil的check方法
        :param self:
        :param ak:
        :param sk:
        :param auth_code:
        :param dict_obj:
        :return:
        """
        items = basic_info()
        items['app_id'] = self._app_id
        items['ak'] = ak
        items['auth_code'] = auth_code
        items['dict_obj'] = dict_obj
        return items
