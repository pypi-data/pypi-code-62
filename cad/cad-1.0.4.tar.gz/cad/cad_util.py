#!/usr/bin/env python
# -*- coding:utf-8 _*-  
"""
@author  : Lin Luo / Bruce Liu
@time    : 2020/2/4 10:28
@contact : 15869300264@163.com
"""
from json import loads

from dynaconf import settings as dynasettings

from .aes_util import AESUtil
from .exceptions import CadException
from .log_util import LogUtil
from .redis_util import RedisUtil


class CadUtil(object):
    def __new__(cls, *args, **kwargs):
        """
        实现单例
        :param args:
        :param kwargs:
        """
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, redis_url_str: str = None, key: str = None, cache_key: str = None, is_log: bool = True):
        """

        :param redis_url_str:
        :param key:
        :param cache_key:
        """
        if redis_url_str is None:
            redis_url_str = dynasettings.REDIS_ADDRESS
        if key is None:
            key = dynasettings.COMMON_SALT
        if cache_key is None:
            self._cache_key = f'{dynasettings.APPLICATION_NAME}:{dynasettings.APP_CONFIG_PREFIX}'
        else:
            self._cache_key = cache_key
        self._redis_client = RedisUtil(url_str=redis_url_str).redis
        self._aes_client = AESUtil(encrypt_key=key)
        self._is_log = is_log

    @LogUtil()
    def get(self, ak: str) -> dict:
        """
        通过ak获取解密后的用户信息
        :param ak:
        :return:
        """
        data = self._redis_client.get(f'{self._cache_key}:{ak}')
        if data is not None:
            data = str(data, 'utf-8')
            return loads(self._aes_client.decrypt(data))
        else:
            raise CadException(ak)
