#coding:utf-8
'''
# File Name: basic.py
# Author: joyle
# mail: joyle.zhang@qq.com
# Created Time: 2020年08月03日 星期一 00时00分00秒
'''
import pandas as pd
from .utils import getList, getFactor

__all__=[
    "list",
    "query",
    "money_flow",
    "cash_flow",
    "shhkt_sharehold",
    "margin_info",
]

GROUP="basic"

def list():
    """ 获取列表

    获取衍生数据列表

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
        key: 衍生数据组合key
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

def money_flow(*, fields=None,isymbol=None,stocks=None,startdate=None,enddate=None,period=None):
    """ 个股资金流向

    获取个股资金流向衍生数据

    Args:
        fields: 衍生数据字段，None表示返回所有字段
        isymbol: 指数
        stocks: 个股列表
        startdate: 起始日期
        enddate: 终止日期
        period: 周期

    Returns:
        (status,ret)
    """
    return getFactor( GROUP, "money_flow", factors=fields, isymbol=isymbol,stocks=stocks,startdate=startdate,enddate=enddate,period=period)

def cash_flow(*, fields=None,isymbol=None,stocks=None,startdate=None,enddate=None,period=None):
    """ 股票资金流向

    获取股票资金流向衍生数据

    Args:
        fields: 衍生数据字段，None表示返回所有字段
        isymbol: 指数
        stocks: 个股列表
        startdate: 起始日期
        enddate: 终止日期
        period: 周期

    Returns:
        (status,ret)
    """
    return getFactor( GROUP, "cash_flow", factors=fields, isymbol=isymbol,stocks=stocks,startdate=startdate,enddate=enddate,period=period)

def shhkt_sharehold(*, fields=None,isymbol=None,stocks=None,startdate=None,enddate=None,period=None):
    """ 沪港通持股记录

    获取沪港通持股记录衍生数据

    Args:
        fields: 衍生数据字段，None表示返回所有字段
        isymbol: 指数
        stocks: 个股列表
        startdate: 起始日期
        enddate: 终止日期
        period: 周期

    Returns:
        (status,ret)
    """
    return getFactor( GROUP, "shhkt_sharehold", factors=fields, isymbol=isymbol,stocks=stocks,startdate=startdate,enddate=enddate,period=period)

def margin_info(*, fields=None,isymbol=None,stocks=None,startdate=None,enddate=None,period=None):
    """ 融资融券明细

    获取融资融券明细衍生数据

    Args:
        fields: 衍生数据字段，None表示返回所有字段
        isymbol: 指数
        stocks: 个股列表
        startdate: 起始日期
        enddate: 终止日期
        period: 周期

    Returns:
        (status,ret)
    """
    return getFactor( GROUP, "margin_info", factors=fields, isymbol=isymbol,stocks=stocks,startdate=startdate,enddate=enddate,period=period)
