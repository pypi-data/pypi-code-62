#coding:utf-8
'''
# File Name: vip_std.py
# Author: joyle
# mail: joyle.zhang@qq.com
# Created Time: 2020年08月03日 星期一 00时00分00秒
'''
import pandas as pd
from ...utils import getList,getFactor

__all__=[
    "list",
    "query",
    "rl_characteristic",
    "dx_securities",
    "tf_securities",
    "inhouse",
]

GROUP="factor/vip/standard"

def list():
    """ 获取列表

    获取因子列表

    Args:
        无

    Returns:
        (status,ret)
    """
    return getList(GROUP)

def query(key, *, fields=None,isymbol=None,stocks=None,startdate=None,enddate=None,period=None):
    """ 通用查询接口

    通用查询接口

    Args:
        key: 因子组key
        fields: 衍生数据字段，None表示返回所有字段
        isymbol: 指数
        stocks: 个股列表
        startdate: 起始日期
        enddate: 终止日期
        period: 周期

    Returns:
        (status,ret)
    """
    return getFactor( GROUP, key, factors=fields, isymbol=isymbol,stocks=stocks,startdate=startdate,enddate=enddate,period=period)

def rl_characteristic(*, fields=None,isymbol=None,stocks=None,startdate=None,enddate=None,period=None):
    """ 融量特色因子

    融量特色因子

    Args:
        fields: 因子数据返回字段，None表示返回所有字段
        isymbol: 指数
        stocks: 个股列表
        startdate: 起始日期
        enddate: 终止日期
        period: 周期

    Returns:
        (status,ret)
    """
    return getFactor( GROUP, "rl_characteristic", factors=fields, isymbol=isymbol,stocks=stocks,startdate=startdate,enddate=enddate,period=period)

def dx_securities(*, fields=None,isymbol=None,stocks=None,startdate=None,enddate=None,period=None):
    """ 东兴因子

    东兴因子

    Args:
        fields: 因子数据返回字段，None表示返回所有字段
        isymbol: 指数
        stocks: 个股列表
        startdate: 起始日期
        enddate: 终止日期
        period: 周期

    Returns:
        (status,ret)
    """
    return getFactor( GROUP, "dx_securities", factors=fields, isymbol=isymbol,stocks=stocks,startdate=startdate,enddate=enddate,period=period)

def tf_securities(*, fields=None,isymbol=None,stocks=None,startdate=None,enddate=None,period=None):
    """ 天风因子

    天风因子

    Args:
        fields: 因子数据返回字段，None表示返回所有字段
        isymbol: 指数
        stocks: 个股列表
        startdate: 起始日期
        enddate: 终止日期
        period: 周期

    Returns:
        (status,ret)
    """
    return getFactor( GROUP, "tf_securities", factors=fields, isymbol=isymbol,stocks=stocks,startdate=startdate,enddate=enddate,period=period)

def inhouse(*, fields=None,isymbol=None,stocks=None,startdate=None,enddate=None,period=None):
    """ 收费因子

    收费因子

    Args:
        fields: 因子数据返回字段，None表示返回所有字段
        isymbol: 指数
        stocks: 个股列表
        startdate: 起始日期
        enddate: 终止日期
        period: 周期

    Returns:
        (status,ret)
    """
    return getFactor( GROUP, "inhouse", factors=fields, isymbol=isymbol,stocks=stocks,startdate=startdate,enddate=enddate,period=period)
