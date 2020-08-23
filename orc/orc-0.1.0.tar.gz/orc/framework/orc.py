# Author: Jingping.zhao

import json
import traceback
from requests.models import Response
import lazyxml

from framework.exception import OrcException
from framework.lib.common import OrcDefaultDict
from framework.exception import OrcLibraryException


class Orc:
    """
    Basic
    """
    @staticmethod
    def api(p_func):
        """
        :param p_func:
        :return:
        """
        def api_func(*args, **kwargs):
            result = OrcResult()
            try:
                result.set_data(p_func(*args, **kwargs))
            except OrcException as err:
                result.set_code(err.code)
                result.set_message(err.info)
            except Exception:
                result.set_code(0x01)
                result.set_message("Unknown error")

            return result.rtn()

        return api_func

    @staticmethod
    def orc_singleton(cls):
        """
        单例
        :param cls:
        :return:
        """
        instances = {}

        def _singleton(*args, **kw):
            if cls not in instances:
                instances[cls] = cls(*args, **kw)

            return instances[cls]

        return _singleton


class OrcResult(object):
    """
    处理返回值
    """
    def __init__(self, p_res=None):

        object.__init__(self)

        # Status
        self.code = 0x00000000

        # Message
        self.message = ""

        # Data
        self.data = ""

        self.init_res(p_res)

    def __str__(self):
        return "<code: %x, message: %s, data: %s>" % (self.code, self.message, self.code)

    def init_res(self, p_res=None):
        """
        :param p_res:
        :return:
        """
        # 加载并处理返回值
        if p_res is None:
            return

        if isinstance(p_res, OrcException):
            self.code = p_res.code
            self.message = p_res.info

        if isinstance(p_res, Response):
            if not p_res.ok:
                self.code = p_res.status_code
                self.message = p_res.content
            else:
                _res = OrcDefaultDict(json.loads(p_res.content)
                                      if not isinstance(p_res.content, dict) else p_res.content)
                self.code = _res.value("code")
                self.message = _res.value("message")
                self.data = _res.value("data")

    def set_code(self, p_status):
        """
        Set status
        :param p_status:
        :return:
        """
        self.code = p_status

    def set_data(self, p_data):
        """
        Set data
        :param p_data:
        :return:
        """
        self.data = p_data

    def set_message(self, p_message):
        """
        设置返回信息
        :param p_message:
        :return:
        """
        self.message = p_message

    def reset(self):
        """
        重置数据
        :return:
        """
        self.code = 0x00000000
        self.data = ""
        self.message = ""

    def ok(self):
        return self.code == 0x00000000

    def rtn(self):
        """
        返回信息字符串
        :return:
        """
        return dict(code=self.code,
                    message=self.message,
                    data=self._covert_byte(self.data))

    def _covert_byte(self, p_data):
        """
        :param p_data:
        :return:
        """
        if isinstance(p_data, dict):
            return {_key: self._covert_byte(p_data[_key]) for _key in p_data}

        elif isinstance(p_data, list):
            return [self._covert_byte(_item) for _item in p_data]

        elif isinstance(p_data, bytes):
            return str(p_data, encoding="utf-8")

        else:
            return p_data
