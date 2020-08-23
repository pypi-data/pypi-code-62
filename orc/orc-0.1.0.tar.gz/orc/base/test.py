# Author: Jingping.zhao

import copy
import sys
from base.resource import OrcResource


class TestBaseResource(object):
    """
    Base resource test tool
    """
    def __init__(self, p_resource, p_version, *before):
        object.__init__(self)

        self._resource = OrcResource(p_resource, p_version, *before)

        # Id lib, removed these item in teardown
        self._ids = []

        # Result lib, shared in functions
        self._result = {}

    def get_result(self, p_key):
        """
        :param p_key:
        :return:
        """
        return self._result[p_key].data

    def record(self, p_name, p_result):
        """
        :param p_name:
        :param p_result:
        :return:
        """
        if isinstance(p_result.data, dict):
            self._ids.append(p_result.data["id"])
            self._result[p_name] = p_result

    def clean(self):
        """
        :return:
        """
        self.base_delete({"id": self._ids})

    @staticmethod
    def print_res(res):
        """
        :param res:
        :return:
        """
        print("Code: %s" % res.code)
        print("Message: %s" % res.message)
        print("Data: %s" % res.data)
        print()

    def base_help(self):
        """
        :return:
        """
        result = self._resource.fetch("help", {})
        self.print_res(result)
        assert 0 == result.code

    def base_add(self, p_data):
        """
        :param p_data:
        :return:
        """
        result = self._resource.add(p_data)
        self.print_res(result)
        assert 0 == result.code
        assert "id" in result.data

        return result

    def base_add_fail(self, p_data):
        """
        :param p_data:
        :return:
        """
        result = self._resource.add(p_data)
        self.print_res(result)
        assert 0 != result.code

        return result

    def base_delete(self, p_data):
        """
        :param p_data:
        :return:
        """
        result = self._resource.delete(p_data)
        self.print_res(result)
        assert 0 == result.code
        assert result.data

        return result

    def base_delete_fail(self, p_data):
        """
        :param p_data:
        :return:
        """
        result = self._resource.delete(p_data)
        self.print_res(result)
        assert 0 != result.code

        return result

    def base_delete_one(self, p_id):
        """
        :param p_id:
        :return:
        """
        result = self._resource.id(p_id).delete({})
        self.print_res(result)
        assert 0 == result.code
        assert result.data

        return result

    def base_delete_one_fail(self, p_id):
        """
        :param p_id:
        :return:
        """
        result = self._resource.id(p_id).delete({})
        self.print_res(result)
        assert 0 != result.code

        return result

    def base_update(self, p_id, p_data):
        """
        :param p_id:
        :param p_data:
        :return:
        """
        result = self._resource.id(p_id).update(p_data)
        self.print_res(result)
        assert 0 == result.code
        assert result.data
        return result

    def base_update_fail(self, p_id, p_data):
        """
        :param p_id:
        :param p_data:
        :return:
        """
        result = self._resource.id(p_id).update(p_data)
        self.print_res(result)
        assert 0 != result.code
        return result

    def base_query(self, p_data):
        """
        :param p_data:
        :return:
        """
        result = self._resource.query(p_data)
        self.print_res(result)
        assert 0 == result.code

        return result

    def base_query_fail(self, p_data):
        """
        :param p_data:
        :return:
        """
        result = self._resource.query(p_data)
        self.print_res(result)
        assert 0 == result.code
        assert not result.data

        return result

    def base_query_one(self, p_id, p_data=None):
        """
        :param p_data:
        :param p_id: id
        :return:
        """
        result = self._resource.id(p_id).query(p_data or {})
        self.print_res(result)
        assert 0 == result.code
        assert isinstance(result.data, dict)
        return result

    def base_query_one_fail(self, p_id, p_data=None):
        """
        :param p_data:
        :param p_id: id
        :return:
        """
        result = self._resource.id(p_id).query(p_data or {})
        self.print_res(result)
        assert 0 == result.code
        assert result.data is None
        return result

    def base_fetch(self, p_func, p_data):
        """
        :param p_func:
        :param p_data:
        :return:
        """
        result = self._resource.fetch(p_func, p_data)
        self.print_res(result)
        assert 0 == result.code

        return result

    def base_fetch_fail(self, p_func, p_data):
        """
        :param p_func:
        :param p_data:
        :return:
        """
        result = self._resource.fetch(p_func, p_data)
        self.print_res(result)
        assert 0 != result.code

        return result

    def base_fetch_one(self, p_func, p_id, p_data):
        """
        :param p_func:
        :param p_id:
        :param p_data:
        :return:
        """
        result = self._resource.id(p_id).fetch(p_func, p_data)
        self.print_res(result)
        assert 0 == result.code

        return result

    def base_fetch_one_fail(self, p_func, p_id, p_data):
        """
        :param p_func:
        :param p_id:
        :param p_data:
        :return:
        """
        result = self._resource.id(p_id).fetch(p_func, p_data)
        self.print_res(result)
        assert 0 != result.code

        return result


class TestDefaultResource(TestBaseResource):
    """
    Resource test tool with default data
    """
    def __init__(self, p_resource, p_version, *before):
        TestBaseResource.__init__(self, p_resource, p_version, *before)

        self._default_data = {}

    def set_default(self, p_func: str, p_data: dict):
        """
        :param p_func:
        :param p_data:
        :return:
        """
        self._default_data[p_func] = p_data

    def _data(self, p_func: str, p_data=None):
        """
        :param p_func:
        :param p_data:
        :return:
        """
        data_output = {}
        data_base = {}

        if p_data is not None:
            data_output = copy.deepcopy(p_data)

        if p_func in self._default_data:
            data_base = copy.deepcopy(self._default_data[p_func])

        for _key, _value in data_base.items():
            if _key not in data_output:
                data_output[_key] = _value

        return data_output

    def default_add(self, p_data=None):
        """
        :param p_data:
        :return:
        """
        return self.base_add(self._data("add", p_data))

    def default_add_fail(self, p_data=None):
        """
        :param p_data:
        :return:
        """
        return self.base_add_fail(self._data("add", p_data))

    def default_update(self, p_id, p_data=None):
        """
        :param p_id:
        :param p_data:
        :return:
        """
        return self.base_update(p_id, self._data("update", p_data))

    def default_update_fail(self, p_id, p_data=None):
        """
        :param p_id:
        :param p_data:
        :return:
        """
        return self.base_update_fail(p_id, self._data("update", p_data))

    def default_query(self, p_data=None):
        """
        :param p_data:
        :return:
        """
        return self.base_query(self._data("query", p_data))

    def default_query_fail(self, p_data=None):
        """
        :param p_data:
        :return:
        """
        return self.base_query_fail(self._data("query", p_data))

    def default_fetch(self, p_func, p_data=None):
        """
        :param p_func:
        :param p_data:
        :return:
        """
        return self.base_fetch(p_func, self._data(p_func, p_data))

    def default_fetch_fail(self, p_func, p_data=None):
        """
        :param p_func:
        :param p_data:
        :return:
        """
        return self.base_fetch_fail(p_func, self._data(p_func, p_data))

    def default_fetch_one(self, p_func, p_id, p_data=None):
        """
        :param p_id:
        :param p_func:
        :param p_data:
        :return:
        """
        return self.base_fetch_one(p_func, p_id, self._data(p_func, p_data))

    def default_fetch_one_fail(self, p_func, p_id, p_data=None):
        """
        :param p_id:
        :param p_func:
        :param p_data:
        :return:
        """
        return self.base_fetch_one_fail(p_func, p_id, self._data(p_func, p_data))


class UtilTest:
    """
    Test info
    """
    @staticmethod
    def test_start():
        """
        :return:
        """
        case_name = sys._getframe(1).f_code.co_name
        size = 67 - len(case_name)
        before = size // 2
        end = size - before
        print(("-" * before) + " Start case %s " % case_name + ("-" * end))

    @staticmethod
    def test_end():
        """
        :return:
        """
        print(("-" * 37) + " End " + ("-" * 38))
        print()
