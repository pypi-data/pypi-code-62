# Author: Jingping.zhao

import json
import requests
from app import application
from framework.orc import OrcResult
from framework.lib.config import ResourceConfig
from base.exception import BaseResourceException


class OrcResource(object):
    """
    Resource client
    """
    def __init__(self, p_flag: str, p_version: str = "1.0", *p_source):

        self._header = {'content-type': "application/json"}

        self._flag = p_flag
        self._args_id = None
        self._source = p_source if p_source else ()
        self._version = p_version

        self._resource_config = ResourceConfig(self._flag, self._version)

        keys = ["scheme", "host", "port", "group", "funcs"]
        for _key in keys:
            _cfg = getattr(self._resource_config, _key, None)
            if _cfg is None:
                raise BaseResourceException(0x2, "Configuration %s is not found for %s." % (_key, self._flag))

        funcs = eval(self._resource_config.funcs)
        if not isinstance(funcs, list):
            raise BaseResourceException(0x1, "Config %s.funcs is wrong." % self._flag)

        for _name in funcs:
            setattr(self, _name, self._create_func(_name))

    def _create_func(self, p_func):
        """
        :param p_func: func name
        :return:
        """

        def func(p_data):
            """
            :return:
            """
            return getattr(self, "fetch")(p_func, p_data)

        return func

    def _url(self) -> str:
        """
        :return:
        """
        param_list = [
            "%s://%s:%s" % (self._resource_config.scheme,
                            self._resource_config.host,
                            self._resource_config.port),
            self._resource_config.group,
            self._version,
            self._flag]
        param_list.extend(self._path())
        param_list = [str(i) for i in param_list]
        return "/".join(param_list)

    def _path(self):
        """
        :return:
        """
        args = []
        if isinstance(self._source, str):
            args.append(self._source)
        else:
            args.extend(self._source)
        if self._args_id:
            args.append(self._args_id)
            self._args_id = None

        return args

    def id(self, p_id):
        """
        :param p_id:
        :return:
        """
        self._args_id = p_id
        return self

    def debug(self):
        """
        :return:
        """
        return {
            "url": self._url(),
            "headers": self._header
        }

    def fetch(self, method, data):
        """
        :param method:
        :param data:
        :return:
        """
        return OrcResult(
            requests.post(url=self._url(),
                          headers=self._header,
                          params={"method": method},
                          data=json.dumps(data)))
