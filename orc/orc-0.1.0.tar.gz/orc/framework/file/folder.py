# Author: Jingping.zhao

import os
import time
from framework.exception import OrcFrameworkLibException


class FileLib(object):
    """
    File Library
    """
    def __init__(self, p_path: str, p_extend: str = None):
        object.__init__(self)

        self._path = p_path
        self._extend = "" if not p_extend else "." + p_extend

        if not os.path.exists(self._path):
            os.mkdir(p_path)

    def save(self, p_data: str, p_name: str = None):
        """
        :param p_name:
        :param p_data:
        :return:
        """
        if p_name is not None:
            file_name = p_name
            file_path = os.path.join(self._path, file_name + self._extend)
            if os.path.exists(file_path):
                raise OrcFrameworkLibException(0x1, "File %s is already exists.")
        else:
            for i in range(10):
                file_name = time.strftime("%Y%m%d%H%M%S", time.localtime())
                file_path = os.path.join(self._path, file_name + self._extend)
                if not os.path.exists(file_name):
                    break
            else:
                raise OrcFrameworkLibException(0x1, "Generate new file name failed.")

        with open(file_path, "w") as _file:
            _file.write(p_data)

        return {"file": file_name}

    def recover(self, p_data: str, p_name: str = None):
        """
        :param p_name:
        :param p_data:
        :return:
        """
        file_name = p_name or time.strftime("%Y%m%d%H%M%S", time.localtime())
        file_path = os.path.join(self._path, file_name + self._extend)

        with open(os.path.join(self._path, file_path), "w") as _file:
            _file.write(p_data)

        return {"file": file_name}

    def read(self, p_name: str):
        """
        :param p_name:
        :return:
        """
        file_path = os.path.join(self._path, p_name + self._extend)
        with open(os.path.join(self._path, file_path), "r") as _file:
            content = _file.readlines()
        return "".join(content)

    def remove(self, p_name: str):
        """
        :param p_name:
        :return:
        """
        file_path = os.path.join(self._path, p_name + self._extend)
        if os.path.exists(file_path):
            os.remove(file_path)
