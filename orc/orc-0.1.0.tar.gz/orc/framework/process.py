# Author: Jingping.zhao, 2020.07.14

from app import application
from framework.database.table import OrcOrderTable, OrcTable
from framework.database.tree import OrcTree, OrcOrderTree, OrcUniqueTree
from framework.exception import OrcFrameworkProcessException
from framework.lib.OrcString import OrcNameStr


class OrcProcess(object):
    """
    Business pipeline
    """
    def __init__(self, p_type: str = None, p_funcs: list = None):
        object.__init__(self)

        self._resource = None
        self._process = type("OrcTempResource", (), {})
        self._table = type("OrcTempResource", (), {})

        # Import resource
        self._init_resource(p_type)

        # Initialize functions
        self._init_funcs(p_funcs)

    def _init_resource(self, p_type: str):
        """
        :param p_type:
        :return:
        """
        if p_type is None:
            return

        # try:
        cls_name = self.__class__.__name__
        self._resource = self._get_table(p_type, cls_name)

    def _init_funcs(self, p_funcs: list):
        """
        :param p_funcs:
        :return:
        """
        if p_funcs is None:
            return

        for _name in p_funcs:
            setattr(self, _name, self._create_func(_name))

    def _create_func(self, p_func: str):
        """
        :param p_func: func name
        :return:
        """
        def func(p_data):
            """
            :return:
            """
            resource = getattr(self, "_resource")
            return p_func if resource is None else getattr(resource, p_func)(p_data)

        return func

    def import_table(self, p_key, p_flag, p_type: str = "TABLE"):
        """
        :param p_type:
        :param p_flag:
        :param p_key:
        :return:
        """
        try:
            setattr(self._table, p_key, self._get_table(p_type, p_flag))
        except (ImportError, ModuleNotFoundError):
            raise OrcFrameworkProcessException(0x1, "Table $s is not found." % p_flag)

    def import_resource(self, p_flag: str, p_type: str = "PROC"):
        """
        :param p_flag:
        :param p_type:
        :return:
        """
        try:
            if "PROC" == p_type:
                self._resource = self._get_process(p_flag)
            else:
                self._resource = self._get_table(p_type, p_flag)
        except (ImportError, ModuleNotFoundError):
            raise OrcFrameworkProcessException(0x1, "Table $s is not found." % p_flag)

    def import_process(self, p_flag, p_key):
        """
        :param p_key:
        :param p_flag:
        :return:
        """
        try:
            setattr(self._process, p_key, self._get_process(p_flag))
        except (ImportError, ModuleNotFoundError):
            raise OrcFrameworkProcessException(0x1, "Table $s is not found." % p_flag)

    @staticmethod
    def _get_table(p_type, p_flag):
        """
        :param p_type:
        :param p_flag:
        :return:
        """
        tables = {
            "TABLE": OrcTable,
            "ORDER-TABLE": OrcOrderTable,
            "TREE": OrcTree,
            "ORDER-TREE": OrcOrderTree,
            "UNIQUER-TREE": OrcUniqueTree
        }
        return tables[p_type](OrcNameStr().from_module_name(p_flag).class_name())

    @staticmethod
    def _get_process(p_flag):
        """
        :param p_flag:
        :return:
        """
        cls_info = OrcNameStr().from_module_flag(p_flag)
        return __import__("process.%s" % cls_info.process_name(), {}, {},
                          ["modules"]).__getattribute__(cls_info.process_name())()
