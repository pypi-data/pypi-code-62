# -*- coding: utf-8 -*-

import datetime
from django.db import connections
from django.db import transaction
from collections import namedtuple
import copy


class LogHelper:
    @staticmethod
    def log_method(method):
        print('--------------------------------------------')
        print('method: %s' % method)
        print('--------------------------------------------')


class TimeDeltaHelper:
    @staticmethod
    def time_delta():
        now_date = datetime.datetime.utcnow()
        timedel = now_date + datetime.timedelta(days=-90)
        return timedel

    @staticmethod
    def time_delta_week():
        now_date = datetime.datetime.utcnow()
        timedel = now_date + datetime.timedelta(days=-7)
        return timedel

    @staticmethod
    def time_delta_month():
        now_date = datetime.datetime.utcnow()
        timedel = now_date + datetime.timedelta(days=-30)
        return timedel

    @staticmethod
    def time_delta_month_3():
        now_date = datetime.datetime.utcnow()
        timedel = now_date + datetime.timedelta(days=-90)
        return timedel

    @staticmethod
    def days(day1, day2):
        num = (day2 - day1).days
        return num

    @staticmethod
    def months(day1, day2):
        num = (day2.year - day1.year) * 12 + day2.month - day1.month
        return num

    @staticmethod
    def dateDiffInHours(t1, t2):
        td = t2 - t1
        return td.days * 24 + td.seconds / 3600 + 1

    @staticmethod
    def db_convert2bj(dtnow):
        nw = datetime.datetime.now()
        try:
            nw = dtnow + datetime.timedelta(hours=+8)
            return nw
        except Exception as ex:
            return nw

    @staticmethod
    def bj_convet2db(dtnow):
        nw = datetime.datetime.now()
        try:
            nw = dtnow + datetime.timedelta(hours=-8)
            return nw
        except Exception as ex:
            return nw

    @staticmethod
    def formate_date2mid(date_value):
        res = '%04d-%02d-%02d' % (date_value.year, date_value.month, date_value.day)
        return res


class DictHelper:
    @staticmethod
    def convert_to_dicts(objs):
        """

        :param objs:
        :return:

        把对象列表转换为字典列表
        """

        obj_arr = []

        for o in objs:
            # 把Object对象转换成Dict
            dict = {}
            dict.update(o.__dict__)
            dict.pop("_state", None)  # 去除掉多余的字段
            obj_arr.append(dict)

        return obj_arr

    @staticmethod
    def convert_to_dict(obj):
        """

        :param obj:
        :return:

        把对象转换为DICT
        """
        dict = {}
        dict.update(obj.__dict__)
        dict.pop("_state", None)
        return dict

    @staticmethod
    def transmit(source_obj, target_obj):
        """

        :param source_obj:
        :param target_obj:
        :return:

        使用场景：
            源对象属性多于目标对象。
            删减源对象中多余的属性，赋值给目标对象
        """
        dict_target = {}
        dict_source = {}

        dict_target.update(target_obj.__dict__)
        dict_target.pop("_state", None)

        dict_source.update(source_obj.__dict__)
        dict_source.pop("_state", None)

        dict_swap = {}
        dict_swap = copy.deepcopy(dict_source)

        for key in dict_source.keys():
            if not key in dict_target.keys():
                dict_swap.pop(key, None)

        target_obj.__dict__.update(**dict_swap)

        return target_obj


class Dict2Obj(object):
    """
     将 dict 转换为 object
    """

    def __init__(self, d):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
                setattr(self, a, [Dict2Obj(x) if isinstance(x, dict) else x for x in b])
            else:
                setattr(self, a, Dict2Obj(b) if isinstance(b, dict) else b)


class FormHelper:
    """
     用于为Form提供帮助
    """

    @staticmethod
    def initialize(model, form):
        """

        :param model:
        :param form:
        :return:

        根据 model 给form赋初值
        """
        data = {}
        for key in form.fields:
            data[key] = model.__dict__.get(key, None)

        return data


class DbHelper:
    @staticmethod
    def namedtuplefetchall(cursor):
        "Return all rows from a cursor as a namedtuple"
        desc = cursor.description
        nt_result = namedtuple('Result', [col[0] for col in desc])
        return [nt_result(*row) for row in cursor.fetchall()]

    @staticmethod
    def dictfetchall(cursor):
        "Return all rows from a cursor as a dict"
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    @staticmethod
    def execute(sql, conn=None):
        if not conn:
            conn = connections['default']
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql)
        except Exception as ex:
            raise ex
        finally:
            conn.close()

    @staticmethod
    def query(sql, conn=None):
        results = None
        if not conn:
            conn = connections['default']
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                results = DbHelper.namedtuplefetchall(cursor)
        except Exception as ex:
            raise ex
        finally:
            conn.close()

        return results

    @staticmethod
    def query_with_titles(sql, conn=None):
        data = {}
        data_list = []
        if not conn:
            conn = connections['default']
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql)

                for field in cursor.description:
                    data_list.append(field[0])

                results = DbHelper.namedtuplefetchall(cursor)
        except Exception as ex:
            raise ex
        finally:
            conn.close()

        data['titles'] = data_list
        data['results'] = results
        return data

    @staticmethod
    def get_titles(cursor_description):
        data_list = []
        for field in cursor_description:
            data_list.append(field[0])
        return data_list
