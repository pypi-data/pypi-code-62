# Author: Jingping.zhao
import copy

from ..framework.lib.config import LocalConfig
from .resource import OrcResource


class ConfigClient(object):
    """
    Get config
    """
    def __init__(self):
        object.__init__(self)

        version = LocalConfig.get_config_info()["version"]
        self._resource = OrcResource("sys-config", version)

    def _get(self, p_path: str, p_env: str = "DEFAULT"):
        """
        :param p_path:
        :param p_env:
        :return:
        """
        result = self._resource.config({"path": p_path, "env": p_env})
        return None if 0 != result.code else result.data

    @staticmethod
    def get(p_path: str, p_env: str = "DEFAULT"):
        """
        :param p_path:
        :param p_env:
        :return:
        """
        inst = ConfigClient()
        return inst._get(p_path, p_env)


class ServiceConfigClient(object):
    """
    Configuration for current service
    """
    def __init__(self, p_service_name):
        object.__init__(self)

        service_name = p_service_name
        self._config_default = ConfigClient.get("system.service.%s" % service_name)
        self._config_env = ConfigClient.get("system.service.%s" % service_name, LocalConfig.get_env())

    def get_config(self):
        """
        :return:
        """
        configs = copy.deepcopy(self._config_default)
        for _flag, _flag_value in self._config_env.items():
            if _flag not in configs:
                configs[_flag] = _flag_value
                continue
            for _key, _value in _flag_value.items():
                configs[_flag][_key] = _value

        return configs
