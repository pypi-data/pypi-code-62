# Author: Jingping.zhao


class OrcDefaultDict(object):
    """
    有默认值字典
    """
    def __init__(self, data_dict=None, default=None, func=None):

        # 字典数据
        self._data = dict()

        # 执行函数
        self._func = func

        # 默认值
        self._default = default

        if isinstance(data_dict, dict):
            self._data = data_dict

    def init(self, data_dict=None, default=None, func=None):
        """
        初始化
        :param func:
        :param default:
        :param data_dict:
        :return:
        """
        # 执行函数
        self._func = func

        # 默认值
        self._default = default

        if isinstance(data_dict, dict):
            self._data = data_dict

    def value(self, p_key, p_default=None):
        """
        值
        :param p_key:
        :param p_default:
        :return:
        """
        self._default = p_default

        if not isinstance(self._data, dict):
            return self._default

        if p_key not in self._data:
            return self._default

        if self._func is None:
            return self._data[p_key]
        else:
            return self._func(self._data[p_key])

    def add(self, p_key, p_value):
        """
        增加一条数据
        :param p_key:
        :param p_value:
        :return:
        """
        self._data[p_key] = p_value

    def delete(self, p_key):
        """
        删除
        :param p_key:
        :return:
        """
        self._data.pop(p_key)

    def items(self):
        """
        迭代器
        :return:
        """
        return self._data.items()

    def keys(self):
        """
        迭代 Key
        :return:
        """
        return self._data.keys()

    def dict(self):
        """
        返回字典
        :return:
        """
        return self._data


class OrcOrderedDict(object):
    """
    有序字典
    """
    def __init__(self):

        object.__init__(self)

        # 保存数据
        self._order = list()

        # 保存字典
        self._data = OrcDefaultDict()

    def value(self, p_key):
        """
        获取值
        :param p_key:
        :return:
        """
        return self._data.value(p_key)

    def value_by_index(self, p_index):
        """
        通过索引获取值
        :param p_index:
        :type p_index: int
        :return:
        """
        try:
            key = self._order[p_index]
            return self._data.value(key)
        except(TypeError, IndexError):
            return None

    def append(self, p_key, p_value):
        """
        增加一个值
        :param p_value:
        :param p_key:
        :return:
        """
        self._order.append(p_key)
        self._data.add(p_key, p_value)

    def pop(self):
        """
        删除一个值
        :return:
        """
        key = self._order[-1]
        self._order.pop()
        self._data.delete(key)

    def insert(self, p_index, p_key, p_value):
        """
        插入一个值
        :param p_value:
        :param p_key:
        :param p_index:
        :return:
        """
        self._order.insert(p_index, p_key)
        self._data.add(p_key, p_value)

    def delete(self, p_index):
        """
        删除一个值
        :param p_index:
        :return:
        """
        self._order.remove(self._order[p_index])

    def items(self):
        """
        迭代器
        :return:
        """
        for _key in self._order:
            yield _key, self._data.value(_key)

    def keys(self):
        """
        迭代 key
        :return:
        """
        for _key in self._order:
            yield _key

    def dict(self):
        """
        输出 dict
        :return:
        """
        return self._data.dict()
