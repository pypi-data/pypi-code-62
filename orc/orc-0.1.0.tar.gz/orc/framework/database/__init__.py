# Author: Jingping.zhao
# Exception: 0x00 - 0x09

from app import database
from framework.lib.OrcString import OrcNameStr
from framework.lib.common import OrcDefaultDict
from framework.lib.program import SingletonType


class ClsTableLib:
    """
    Table class lib
    """
    _cls_lib = {}
    __metaclass__ = SingletonType

    def _get_table(self, p_flag):
        """
        :param p_flag:
        :return:
        """
        if p_flag not in self._cls_lib:
            self._cls_lib[p_flag] = create_table(p_flag)
        return self._cls_lib[p_flag]

    @classmethod
    def table(cls, p_flag):
        """
        :param p_flag:
        :return:
        """
        return ClsTableLib()._get_table(p_flag)


def create_table(flag):
    """
    Create a table class
    type, length, primary, default
    :param flag:
    :type flag: str
    :return:
    """
    table_flag = OrcNameStr().from_module_flag(flag)
    definition = __import__("definition.table", {}, {}, ["modules"]).__getattribute__(table_flag.table_config_name())

    class Extra:
        """
        Extra table info
        """
        orc_keys = []
        orc_order = ""
        orc_unique = ""
        orc_mandatory = []
        orc_length = {}

    def cls_init(self, data=None):
        """
        Function __init__
        :param self:
        :param data:
        :return:
        """
        _data = OrcDefaultDict(data)
        for _key in definition:
            setattr(self, _key, _data.value(_key))

    def cls_str(self):
        """
        Function __str__
        :param self:
        :return:
        """
        return "<%s>" % " ,".join(["\"%s\": %s" % (_key, getattr(self, _key)) for _key in definition])

    def cls_dict(self):
        """
        Func to_dict
        :param self:
        :return:
        """
        result = {}
        for _key in definition:
            _res = getattr(self, _key)
            if "DateTime" == definition[_key]["type"]:
                result[_key] = "" if not _res else _res.strftime("%Y-%m-%d %H:%M:%S")
            else:
                result[_key] = _res

        return result

    # Table fields
    table_attrs = {}
    table_extra = Extra()

    for _name, _value in definition.items():

        column_args = []
        column_kwargs = {}

        if "String" == _value["type"]:
            column_args.append(getattr(database, "String")(_value["length"]))
        elif "Integer" == _value["type"]:
            column_args.append(getattr(database, "Integer"))
        elif "Boolean" == _value["type"]:
            column_args.append(getattr(database, "Boolean"))
        elif "DateTime" == _value["type"]:
            column_args.append(getattr(database, "DateTime"))
        else:
            pass

        if "primary" in _value:
            column_kwargs["primary_key"] = _value["primary"]

        if "default" in _value:
            column_kwargs["default"] = _value["default"]

        if "unique" in _value:
            column_kwargs["unique"] = _value["unique"]

        if "length" in _value:
            table_extra.orc_length[_name] = _value["length"]

        if "orc_order" in _value and _value["orc_order"]:
            table_extra.orc_order = _name

        if "orc_unique" in _value and _value["orc_unique"]:
            table_extra.orc_unique = _name

        if "orc_key" in _value and _value["orc_key"]:
            table_extra.orc_keys.append(_name)

        if "orc_mandatory" in _value and _value["orc_mandatory"]:
            table_extra.orc_mandatory.append(_name)

        table_attrs[_name] = database.Column(*column_args, **column_kwargs)

    # Create table
    table_attrs["__tablename__"] = table_flag.table_name()
    table_attrs["__table_args__"] = {"useexisting": True}
    table_attrs["seq_flag"] = table_flag.sequence_flag()
    table_attrs["__str__"] = cls_str
    table_attrs["__init__"] = cls_init
    table_attrs["extra"] = table_extra
    table_attrs["to_dict"] = cls_dict

    return type(table_flag.class_name(), (database.Model,), table_attrs)
