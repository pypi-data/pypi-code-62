# Author: Jingping.zhao

import os
import re
import time


class OrcNameStr(object):
    """
    Manage name string
    """
    def __init__(self):
        object.__init__(self)

        self._flag_list = []

    def from_module_flag(self, p_flag):
        """
        :param p_flag: like FuncName001
        :return:
        """
        self._flag_list = [w.lower() for w in re.findall('[A-Z][a-z]*|[0-9]+', p_flag)]
        return self

    def from_module_name(self, p_flag):
        """
        :param p_flag: like FuncNameApi, remove Api from list
        :return:
        """
        module_name_list = [w.lower() for w in re.findall('[A-Z][a-z]*|[0-9]+', p_flag)]
        if "api" == module_name_list[-1] and "list" == module_name_list[-2]:
            self._flag_list = module_name_list[:-2]
        else:
            self._flag_list = module_name_list[:-1]

        return self

    def from_list_api_name(self, p_flag):
        """
        :param p_flag: like FuncNameApi, remove Api from list
        :return:
        """
        self._flag_list = [w.lower() for w in re.findall('[A-Z][a-z]*|[0-9]+', p_flag)][:-2]
        return self

    def class_name(self):
        """
        :return: FuncName001
        """
        return "".join([w.capitalize() for w in self._flag_list])

    def table_class_name(self):
        """
        Table class name
        :return: TabFuncName001
        """
        return "".join([w.capitalize() for w in (["tab"] + self._flag_list)])

    def table_name(self):
        """
        :return: tab_func_name_001
        """
        return "_".join([w for w in (["tab"] + self._flag_list)])

    def table_config_name(self):
        """
        FuncName001 -> FuncName
        :return:
        """
        return re.sub("[0-9]*$", "", "".join([w.capitalize() for w in self._flag_list]))

    def sequence_flag(self):
        """
        func-name-001
        :return:
        """
        return "-".join(self._flag_list)

    def func_flag(self):
        """
        :return:
        """
        return "-".join(self._flag_list)

    def process_name(self):
        """
        FuncNameProc
        :return:
        """
        return "%sProc" % "".join([w.capitalize() for w in self._flag_list])
