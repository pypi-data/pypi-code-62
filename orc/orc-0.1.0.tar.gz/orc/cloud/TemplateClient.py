# Author: Jingping.zhao, 2020.6.30

from base.resource import OrcResource
from cloud.exception import CloudTemplateException


class TemplateClient(object):
    """
    Template client
    """
    def __init__(self):
        object.__init__(self)
        self._resource = OrcResource("util-template")

    def get(self, p_path):
        """
        :param p_path:
        :return:
        """
        result = self._resource.get({"path": p_path})
        if 0 != result.code:
            raise CloudTemplateException(0x1, "Get template failed, path is %s" % p_path)

        return result.data

    def covert(self, p_path: str, p_data):
        """
        :param p_path:
        :param p_data:
        :return:
        """
        result = self._resource.covert({"template": p_path, "data": p_data})
        if 0 != result.code:
            raise CloudTemplateException(0x1, "Template covert failed for %s, %s" % (p_path, p_data))

        return result.data
