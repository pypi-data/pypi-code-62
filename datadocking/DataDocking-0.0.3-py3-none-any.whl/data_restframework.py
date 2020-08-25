# @Time    : 2020/8/24 18:17
# @Author  : alita
# File     : data_restframework.py

from enum import Enum, unique

import records


class CacheProperty(object):
    """
    实现缓存属性功能
    """
    def __init__(self, fun):
        self.fun = fun

    def __get__(self, instance, owner):
        if instance is None:
            return self
        value = self.fun(instance)
        setattr(instance, self.fun.__name__, value)
        return value


@unique
class DataLoadStatic(Enum):
    """
    自定义数据静态变量加载框架
    """

    @classmethod
    def collect_cls_attrs(cls):
        return {k: v for k, v in cls.__dict__.items() if isinstance(v, cls)}

    @CacheProperty
    def all_fields(self):
        return self.collect_cls_attrs()


class DataParse:
    def __init__(self):
        """
        自定义数据解析框架
        """
        self.setup()
        self.process()
        self.teardown()

    def setup(self):
        pass

    def process(self):
        pass

    def teardown(self):
        pass


class DataSave:
    """自定义数据存储框架"""

    @CacheProperty
    def db(self, sql_url_con=None):
        if not isinstance(sql_url_con, str):
            raise SqlUrlConError("sql con url is comply with sqlalchemy's rules")
        return records.Database(sql_url_con)

    @CacheProperty
    def dbs(self, sql_url_cons=None) -> list:
        if not isinstance(sql_url_cons, list):
            raise SqlUrlConError("sql con urls is list")
        return [records.Database(sql_url_con) for sql_url_con in sql_url_cons]

    def save(self, save_sql=None):
        if save_sql is not None:
            self.db.query(save_sql)


class SqlUrlConError(Exception):
    def __init__(self, code):
        raise Exception(code)



