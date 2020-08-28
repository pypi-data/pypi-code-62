#coding:utf-8
'''
# File Name: stock.py
# Author: joyle
# mail: joyle.zhang@qq.com
# Created Time: 2020年08月03日 星期一 00时00分00秒
'''
import pandas as pd
from .utils import client, getFactor

__all__=[
    "trade_date",
    "trade_list",
    "basicinfo",
    "daily_price",
]

GROUP="stocks"

def trade_date(*, exchange=None, date=None):
    """ 最近交易日

    获取最近交易日

    Args:
        exchange: 对应市场代码，默认为None，取上交所(001002)
                '001002': 上海证券交易所
                '001003': 深圳证券交易所
                '001005': 银行间市场
                '001008': 上海期货交易所
                '001009': 中国金融期货交易所
                '001010': 中国外汇交易市场
                '001015': 上海黄金交易所
                '001016': 大连商品交易所
                '001017': 郑州商品交易所
                '001022': 渤海商品交易所
                '001025': 天津贵金属交易所
                '002001': 香港证券交易所
                '003002': 台湾证券交易所
                '101001': 纽约证券交易所
                '101002': 美国纳斯达克市场
                '101003': 美国证券交易所
                '101014': 纽约商业期货交易所
                '101016': 洲际交易所
                '101017': 芝加哥期货交易所
                '104017': 东京证券交易所
                '105001': 伦敦证券交易所（英国）
                '105015': 法兰克福证交所（德国证交所）
                '105030': 卢森堡证券交易所
                '105061': 伦敦金属交易所
                '106001': 澳大利亚证券交易所
                '107032': 多伦多证券交易所

        date: 日期

    Returns:
        (status,ret)
    """
    params=""

    if exchange:
        params = f"{params}&exchange={exchange}"
    if date:
        params = f"{params}&date={date}"

    params = params[1:]
    url = f"/{GROUP}/trade_date?{params}"
    status, ret = client.request("GET", url=url)
    if status==200:
        ret = ret['trade_date']
    return status, ret

def trade_list(*, startdate, enddate=None, period="1d"):
    """ 交易日历表

    获取交易日列表

    Args:
        startdate: 起始日期
        enddate: 终止日期
        period: 周期

    Returns:
        (status,ret)
    """
    params = f"start_date={startdate}"

    if enddate:
        params = f"{params}&end_date={enddate}"

    params = f"{params}&period={period}"

    url = f"/{GROUP}/trade_list?{params}"
    status, ret = client.request("GET", url=url)
    if status==200:
        ret = [x for x in ret['data']]
    return status, ret

def basicinfo(*, stocks):
    """ 证券基本信息

    获取证券证券基本信息

    Args:
        stocks: 个股列表

    Returns:
        (status,ret)
    """
    if not isinstance(stocks,list):
        stocks = [x for x in stocks.split(',') if x]

    if len(stocks) > 1:
        stocks = ','.join(stocks)
        url = f"/{GROUP}/stock_basic?stocks={stocks}"
        status, ret = client.request("GET", url=url)
        if status==200:
            ret=pd.DataFrame(ret['data'])
    else:
        url = f"/{GROUP}/stock_basic/{stocks[0]}"
        status, ret = client.request("GET", url=url)
        if status==200:
            ret=pd.DataFrame(ret['data'])
    return status, ret

def daily_price(*, fields=None,isymbol=None,stocks=None,startdate=None,enddate=None,period=None):
    """ 证券日行情

    获取证券日行情数据

    Args:
        fields: 行情数据字段，None表示返回所有字段
        isymbol: 指数
        stocks: 个股列表
        startdate: 行情起始日期
        enddate: 行情终止日期
        period: 周期

    Returns:
        (status,ret)
    """
    return getFactor( GROUP, "daily_price", factors=fields, isymbol=isymbol,stocks=stocks,startdate=startdate,enddate=enddate,period=period)
