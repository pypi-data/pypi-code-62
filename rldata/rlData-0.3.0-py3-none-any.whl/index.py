#coding:utf-8
'''
# File Name: index.py
# Author: joyle
# mail: joyle.zhang@qq.com
# Created Time: 2020年08月03日 星期一 00时00分00秒
'''
import pandas as pd
from .utils import client

__all__=[
    "list",
    "component",
    "daily_price"
]

GROUP="index"

def list():
    """ 指数列表

    获取指数列表信息

    Args:
        None

    Returns:
        (status,ret)
    """
    url = f"/{GROUP}/list"
    status, ret = client.request("GET", url=url)
    if status==200:
        ret=pd.DataFrame(ret['data'])
    return status, ret

def component(isymbol, *, date=None):
    """ 指数成分股

    获取指数成分股数据

    Args:
        isymbol: 指数
        date: 日期

    Returns:
        (status,ret)
    """
    params = ""

    if date:
        params = f"trade_date={date}"

    url = f"/{GROUP}/component/{isymbol}?{params}"
    status, ret = client.request("GET", url=url)
    if status==200:
        ret=pd.DataFrame(ret['data'])
    return status, ret

def daily_price(isymbol, *, fields=None,startdate=None,enddate=None,period=None):
    """ 指数日行情

    获取指数日行情数据

    Args:
        isymbol: 指数
        fields: 行情数据字段，None表示返回所有字段
        startdate: 行情起始日期
        enddate: 行情终止日期
        period: 周期

    Returns:
        (status,ret)
    """
    params=""

    if fields:
        if isinstance(fields,list):
            fields = ','.join(fields)
        params = f"{params}&fields={fields}"
    if startdate:
        params = f"{params}&startdate={startdate}"
    if enddate:
        params = f"{params}&enddate={enddate}"
    if period:
        params = f"{params}&period={period}"

    params = params[1:]

    url = f"/{GROUP}/daily_price/{isymbol}?{params}"

    status, ret = client.request("GET", url=url)

    if status == 200:
        ret=pd.DataFrame(ret['data'])

    return status, ret
