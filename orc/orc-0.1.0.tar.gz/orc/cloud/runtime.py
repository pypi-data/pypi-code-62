# Author: Jingping.zhao

from framework.lib.program import SingletonType
from framework.exception import OrcFrameworkLibException
from base.resource import OrcResource


class OrcLocalParams(metaclass=SingletonType):
    """
    Parameters with a flag
    """
    def __init__(self):
        object.__init__(self)

        self._resource = OrcResource("util-runtime")
        self._flag = None

    def init(self, p_flag: str):
        """
        :param p_flag:
        :return:
        """
        self._flag = p_flag

    def _set(self, p_key: str, p_value):
        """
        :param p_key:
        :param p_value:
        :return:
        """
        if self._flag is None:
            raise OrcFrameworkLibException(0x1, "Parameter instance is not initialize.")

        if isinstance(p_value, int):
            data_type = "INT"
        elif isinstance(p_value, float):
            data_type = "FLOAT"
        elif isinstance(p_value, bool):
            data_type = "BOOL"
        elif isinstance(p_value, dict):
            data_type = "JSON"
        elif isinstance(p_value, list):
            data_type = "LIST"
        else:
            data_type = "STRING"

        # Query
        query_result = self._resource.query({"flag": self._flag, "key": p_key})
        if 0 != query_result.code:
            raise OrcFrameworkLibException(0x1, "Get local parameter for key %s failed." % p_key)

        if 1 < len(query_result.data):
            raise OrcFrameworkLibException(0x1, "Too many runtime data[%s.%s] founded." % (self._flag, p_key))

        # Data is not exists, add
        if not query_result.data:
            update_result = self._resource.add({"flag": self._flag, "key": p_key, "type": data_type, "value": p_value})

        # Update
        else:
            query_result = query_result.data[0]
            update_result = self._resource.id(query_result["id"]).update({"type": data_type, "value": p_value})

        if 0 != update_result.code:
            raise OrcFrameworkLibException(
                0x1, "Update data {flag: %s, key: %s, value: %s} failed." % (self._flag, p_key, p_value))

        return True

    def _get(self, p_key: str):
        """
        :param p_key:
        :return:
        """
        if self._flag is None:
            raise OrcFrameworkLibException(0x1, "Parameter instance is not initialize.")

        result = self._resource.fetch("get", {"flag": self._flag, "key": p_key})
        if 0 != result.code:
            raise OrcFrameworkLibException(0x1, "Get data %s.%s failed" % (self._flag, p_key))

        if 1 != len(result.data):
            raise OrcFrameworkLibException(0x1, "Data for %s.%s is wrong, %s." % (self._flag, p_key, result.data))

        return result[0]

    @staticmethod
    def set(p_key, p_value):
        """
        :param p_key:
        :param p_value:
        :return:
        """
        cls = OrcLocalParams()
        return cls.set(p_key, p_value)

    @staticmethod
    def get(p_key):
        """
        :param p_key:
        :return:
        """
        cls = OrcLocalParams()
        return cls.get(p_key)


class OrcGlobalParams(metaclass=SingletonType):
    """
    Global params
    """
    def __init__(self):
        self._params = OrcLocalParams()
        self._params.init("_global")
