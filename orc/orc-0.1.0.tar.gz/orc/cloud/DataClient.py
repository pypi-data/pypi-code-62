# Author: Jingping.zhao, 2020.6.29

from base.resource import OrcResource
from cloud.exception import CloudDataException


class DataClient(object):
    """
    Client for data service
    """
    def __init__(self):
        object.__init__(self)

        self._resource = OrcResource("common-data")

    def all(self, p_src_type, p_src_id) -> list:
        """
        :param p_src_type:
        :param p_src_id:
        :return:
        """
        result = self._resource.all({
            "src_type": p_src_type,
            "src_id": p_src_id
        })

        if 0 != result.code:
            raise CloudDataException(0x1, "Get data for %s:%s failed" % (p_src_type, p_src_id))

        # Calculate length of data suite, max order
        max_length = max([item["order"] for item in result.data])
        params = [{} for i in range(max_length)]

        # Redistribute data
        for item in result.data:
            params[item["order"] - 1][item["data_flag"]] = item["value"]

        return params

    def one(self, p_src_type, p_src_id, p_key, p_order=0):
        """
        :param p_src_type:
        :param p_src_id:
        :param p_order:
        :param p_key: data flag
        :return:
        """
        result = self._resource.get({
            "src_type": p_src_type,
            "src_id": p_src_id,
            "data_flag": p_key
        })

        if 0 != result.code:
            raise CloudDataException(0x2, "Get data for %s:%s.%s[%s] failed" % (p_src_type, p_src_id, p_key, p_order))

        if not result.data:
            return None

        return result.data["value"]
