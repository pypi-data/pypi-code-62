# Author: Jingping.zhao

import json
import copy
import requests
import configparser
from framework.orc import OrcResult
from framework.lib.program import SingletonType
from framework.exception import OrcFrameworkLibException, OrcException


class LocalConfig(metaclass=SingletonType):
    """
    Get config from local configuration file
    """
    def __init__(self):
        self._config_info = configparser.ConfigParser()
        self._config_info.read("/etc/owl/server.cfg")

    def get_section(self, p_section):
        """
        :param p_section:
        :return:
        """
        try:
            return self._config_info[p_section]
        except KeyError:
            raise OrcFrameworkLibException(0x1, "Get local config section %s failed." % p_section)

    def get_value(self, p_section, p_key):
        """
        :param p_section:
        :param p_key:
        :return:
        """
        try:
            return self._config_info[p_section][p_key]
        except KeyError:
            raise OrcFrameworkLibException(0x3, "Get local config %s.%s failed." % (p_section, p_key))

    @staticmethod
    def get_config_info():
        """
        :return:
        """
        config = LocalConfig()
        return config.get_section("CONFIG-SERVICE")

    @staticmethod
    def get_env():
        """
        :return:
        """
        config = LocalConfig()
        return config.get_value("SERVER", "env")


class RemoteConfig(object):
    """
    Get resource configuration from config service
    """
    def __init__(self):
        object.__init__(self)

    @property
    def url(self):
        """
        Config url
        :return:
        """
        try:
            base_config_info = LocalConfig.get_config_info()
            return "%s://%s:%s/%s/%s/%s" % \
                   tuple([base_config_info[key] for key in ("scheme", "host", "port", "group", "version", "source")])
        except KeyError:
            raise OrcFrameworkLibException(0x1, "Config configuration is wrong.")

    def get_raw_config(self, p_path, p_env):
        """
        :param p_path:
        :param p_env:
        :return:
        """
        return self._request("config", p_path, p_env)

    def exists(self, p_path, p_env):
        """
        :param p_path:
        :param p_env:
        :return:
        """
        return self._request("exists", p_path, p_env)

    def _request(self, p_method, p_path, p_env):
        """
        :param p_method:
        :param p_path:
        :param p_env:
        :return:
        """
        result = OrcResult(requests.post(
            url=self.url,
            headers={'content-type': "application/json"},
            params={"method": p_method},
            data=json.dumps({"path": p_path, "env": p_env})))

        if not result.ok():
            return None

        return result.data


class ResourceConfig(RemoteConfig):
    """
    Get resource configuration from config service
    """
    def __init__(self, p_flag, p_version):
        RemoteConfig.__init__(self)

        # Service name
        self._flag = p_flag

        # Service configurations
        self._config = {}

        # Api version
        self._version = p_version

        self._generate_config()

    @property
    def url(self):
        """
        Config url
        :return:
        """
        try:
            base_config_info = LocalConfig.get_config_info()
            return "%s://%s:%s/%s/%s/%s" %\
                   tuple([base_config_info[key] for key in ("scheme", "host", "port", "group", "version", "source")])
        except KeyError:
            raise OrcFrameworkLibException(0x1, "Config configuration is wrong.")

    @property
    def group(self):
        """
        :return:
        """
        return None if "group" not in self._config else self._config["group"]

    @property
    def scheme(self):
        """
        :return:
        """
        return self._get_config("scheme")

    @property
    def host(self):
        """
        :return:
        """
        return self._get_config("host")

    @property
    def port(self):
        """
        :return:
        """
        return self._get_config("port")

    @property
    def version(self):
        """
        :return:
        """
        return self._get_config("version")

    @property
    def funcs(self):
        """
        :return:
        """
        return self._get_config("funcs")

    def _get_config(self, p_key):
        """
        :param p_key:
        :return:
        """
        try:
            return None if self._version not in self._config or p_key not in self._config[self._version] \
                else self._config[self._version][p_key]
        except (KeyError, ValueError):
            return None

    def _generate_config(self):
        """
        :return:
        """
        env = LocalConfig.get_env()
        try:
            self._config = self._generate_env_config(env)
        except OrcException:
            pass

        if not self._config and "DEV" == env:
            self._config = self._generate_env_config("TEST")

    def _generate_env_config(self, p_env):
        """
        {
            group
            ver1: {cfg, ...}
            ver2: {cfg, ...}
            ...
        }
        :param p_env:
        :return:
        """
        def _config(p_flag):
            """
            :param p_flag:
            :return:
            """
            return self.get_raw_config("system.service.resource.%s" % p_flag, p_env)

        def _exist(p_flag):
            """
            :param p_flag:
            :return:
            """
            return self.exists("system.service.resource.%s" % p_flag, p_env)

        # Get service config
        result_service = _config("server.%s" % self._flag)

        # Get group
        if not result_service or "group" not in result_service or not isinstance(result_service["group"], str):
            raise OrcFrameworkLibException(0x01, "Group for %s is wrong." % "server.%s" % self._flag)

        group_name = result_service["group"]
        cfg_data = self._arrange(result_service)

        # Check group config
        group_exist_result = _exist("group.%s" % group_name)

        if group_exist_result:

            # Get group config
            result_group = _config("group.%s" % group_name)
            cfg_group = self._arrange(result_group)

            # Combine data
            for _ver in cfg_group:
                if _ver not in cfg_data:
                    cfg_data[_ver] = cfg_group[_ver]
                    continue

                for _key in cfg_group[_ver]:
                    if _key not in cfg_data[_ver]:
                        cfg_data[_ver][_key] = cfg_group[_ver][_key]

        cfg_data["group"] = group_name

        return cfg_data

    @ staticmethod
    def _arrange(p_data: dict):
        """
        {
            version: {config, ...}
        }
        :param p_data:
        :return:
        """
        def cfg_len(p_key):
            if "funcs" == p_key:
                _data = p_data[p_key]
                if not _data:
                    return 0
                elif isinstance(_data[0], list):
                    return len(_data)
                else:
                    return 1

            return 1 if not isinstance(p_data[p_key], list) else len(p_data[p_key])

        temp_data = copy.deepcopy(p_data)

        if "version" not in p_data:
            return {}

        num = cfg_len("version")
        res_list = [{} for i in range(num)]

        # One item, data => [data]
        if 1 == num:
            temp_data = {_k: [_v] if not isinstance(_v, list) else [_v[0]] for _k, _v in p_data.items()}

        # Combine config data by version
        for _key, _value in temp_data.items():

            if "group" == _key:
                continue

            if num != cfg_len(_key):
                raise OrcFrameworkLibException(0x1, "Config %s's length is wrong" % _key)

            for i in range(num):
                res_list[i][_key] = _value[i]

        # Remove version from each config item, version is the key
        result = {i["version"]: i for i in res_list}
        for _key, _value in result.items():
            _value.pop("version")

        return result


class ApplicationConfig(RemoteConfig):
    """
    Application configurations
    """
    def __init__(self, p_server_flag: str):
        """
        :param p_server_flag: [application flag].[host flag]
        """
        RemoteConfig.__init__(self)
        self._config = self._generate_config(p_server_flag)

    def _generate_config(self, p_server_flag: str):
        """
        :return:
        """
        # Parameters
        server_list = p_server_flag.split(".")
        if 2 != len(server_list):
            raise OrcFrameworkLibException(0x1, "Server flag %s is wrong." % p_server_flag)

        application_name, server_name = server_list
        current_env = LocalConfig.get_env()

        # Configurations
        config_def = {
            "server_env": {
                "path": "system.service.%s.%s" % (application_name, server_name),
                "env": current_env
            },
            "server_default": {
                "path": "system.service.%s.%s" % (application_name, server_name),
                "env": "DEFAULT"
            },
            "default_env": {
                "path": "system.service.%s.default" % application_name,
                "env": current_env
            },
            "default_default": {
                "path": "system.service.%s.default" % application_name,
                "env": "DEFAULT"
            },
        }

        # Config data
        config_raw = {}
        for _key, _value in config_def.items():
            config_raw[_key] = self.get_raw_config(_value["path"], _value["env"])
            if config_raw[_key] is None:
                config_raw[_key] = {}

        # Combine data
        return self._combine(
            self._combine(config_raw["server_env"], config_raw["server_default"]),
            self._combine(config_raw["default_env"], config_raw["default_default"])
        )

    @staticmethod
    def _combine(p_main: dict, p_backup: dict):
        """
        :return:
        """
        configs = copy.deepcopy(p_main)
        for _flag, _flag_value in p_backup.items():
            if _flag not in configs:
                configs[_flag] = _flag_value
                continue
            for _key, _value in _flag_value.items():
                if _key not in configs[_flag]:
                    configs[_flag][_key] = _value

        return configs

    def get_configs(self):
        """
        :return:
        """
        return self._config
