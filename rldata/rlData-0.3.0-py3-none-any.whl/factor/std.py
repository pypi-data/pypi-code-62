#coding:utf-8
'''
# File Name: factor.py
# Author: joyle
# mail: joyle.zhang@qq.com
# Created Time: 2020年08月03日 星期一 00时00分00秒
'''
import pandas as pd
from ..utils import getList, getFactor

__all__=[
    "list",
    "query",
    "basic_derivation",
    "valuation_estimation",
    "reversal",
    "sentiment",
    "power_volume",
    "price_volume",
    "momentum",
    "volatility_value",
    "earning_expectation",
    "solvency",
    "operation_capacity",
    "capital_structure",
    "per_share_indicators",
    "revenue_quality",
    "cash_flow",
    "historical_growth",
    "earning",
]

GROUP="factor/standard"

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

def basic_derivation(*, fields=None,isymbol=None,stocks=None,startdate=None,enddate=None,period=None):
    """ 基础衍生

    获取基础衍生

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
    return getFactor( GROUP, "basic_derivation", factors=fields, isymbol=isymbol,stocks=stocks,startdate=startdate,enddate=enddate,period=period)

def valuation_estimation(*, fields=None,isymbol=None,stocks=None,startdate=None,enddate=None,period=None):
    """ 估值因子

    估值因子

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
    return getFactor( GROUP, "valuation_estimation", factors=fields, isymbol=isymbol,stocks=stocks,startdate=startdate,enddate=enddate,period=period)

def reversal(*, fields=None,isymbol=None,stocks=None,startdate=None,enddate=None,period=None):
    """ 反转指标

    反转指标

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
    return getFactor( GROUP, "reversal", factors=fields, isymbol=isymbol,stocks=stocks,startdate=startdate,enddate=enddate,period=period)

def sentiment(*, fields=None,isymbol=None,stocks=None,startdate=None,enddate=None,period=None):
    """ 情绪指标

    情绪指标

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
    return getFactor( GROUP, "sentiment", factors=fields, isymbol=isymbol,stocks=stocks,startdate=startdate,enddate=enddate,period=period)

def power_volume(*, fields=None,isymbol=None,stocks=None,startdate=None,enddate=None,period=None):
    """ 量能指标

    量能指标

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
    return getFactor( GROUP, "power_volume", factors=fields, isymbol=isymbol,stocks=stocks,startdate=startdate,enddate=enddate,period=period)

def price_volume(*, fields=None,isymbol=None,stocks=None,startdate=None,enddate=None,period=None):
    """ 量价指标

    量价指标

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
    return getFactor( GROUP, "price_volume", factors=fields, isymbol=isymbol,stocks=stocks,startdate=startdate,enddate=enddate,period=period)

def momentum(*, fields=None,isymbol=None,stocks=None,startdate=None,enddate=None,period=None):
    """ 动量指标

    动量指标

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
    return getFactor( GROUP, "momentum", factors=fields, isymbol=isymbol,stocks=stocks,startdate=startdate,enddate=enddate,period=period)

def volatility_value(*, fields=None,isymbol=None,stocks=None,startdate=None,enddate=None,period=None):
    """ 收益风险

    收益风险

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
    return getFactor( GROUP, "volatility_value", factors=fields, isymbol=isymbol,stocks=stocks,startdate=startdate,enddate=enddate,period=period)

def earning_expectation(*, fields=None,isymbol=None,stocks=None,startdate=None,enddate=None,period=None):
    """ 盈利预测

    盈利预测

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
    return getFactor( GROUP, "earning_expectation", factors=fields, isymbol=isymbol,stocks=stocks,startdate=startdate,enddate=enddate,period=period)

def solvency(*, fields=None,isymbol=None,stocks=None,startdate=None,enddate=None,period=None):
    """ 偿债能力

    偿债能力

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
    return getFactor( GROUP, "solvency", factors=fields, isymbol=isymbol,stocks=stocks,startdate=startdate,enddate=enddate,period=period)

def operation_capacity(*, fields=None,isymbol=None,stocks=None,startdate=None,enddate=None,period=None):
    """ 营运能力

    营运能力

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
    return getFactor( GROUP, "operation_capacity", factors=fields, isymbol=isymbol,stocks=stocks,startdate=startdate,enddate=enddate,period=period)

def capital_structure(*, fields=None,isymbol=None,stocks=None,startdate=None,enddate=None,period=None):
    """ 资本结构

    资本结构

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
    return getFactor( GROUP, "capital_structure", factors=fields, isymbol=isymbol,stocks=stocks,startdate=startdate,enddate=enddate,period=period)

def per_share_indicators(*, fields=None,isymbol=None,stocks=None,startdate=None,enddate=None,period=None):
    """ 每股指标

    每股指标

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
    return getFactor( GROUP, "per_share_indicators", factors=fields, isymbol=isymbol,stocks=stocks,startdate=startdate,enddate=enddate,period=period)

def revenue_quality(*, fields=None,isymbol=None,stocks=None,startdate=None,enddate=None,period=None):
    """ 收益质量

    收益质量

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
    return getFactor( GROUP, "revenue_quality", factors=fields, isymbol=isymbol,stocks=stocks,startdate=startdate,enddate=enddate,period=period)

def cash_flow(*, fields=None,isymbol=None,stocks=None,startdate=None,enddate=None,period=None):
    """ 现金流量

    现金流量

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
    return getFactor( GROUP, "cash_flow", factors=fields, isymbol=isymbol,stocks=stocks,startdate=startdate,enddate=enddate,period=period)

def historical_growth(*, fields=None,isymbol=None,stocks=None,startdate=None,enddate=None,period=None):
    """ 历史成长

    历史成长

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
    return getFactor( GROUP, "historical_growth", factors=fields, isymbol=isymbol,stocks=stocks,startdate=startdate,enddate=enddate,period=period)

def earning(*, fields=None,isymbol=None,stocks=None,startdate=None,enddate=None,period=None):
    """ 盈利能力

    盈利能力

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
    return getFactor( GROUP, "earning", factors=fields, isymbol=isymbol,stocks=stocks,startdate=startdate,enddate=enddate,period=period)
