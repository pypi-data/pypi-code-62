#coding:utf-8
'''
# File Name: tools.py
# Author: joyle
# mail: joyle.zhang@qq.com
# Created Time: 2020年08月03日 星期一 00时00分00秒
'''
import pandas as pd
from .client import client

__all__=[
    "getList",
    "getFactor",
    "FactorApiGenerator",
]

def getList(group):
    """
    
    """
    url = f"/{group}/"

    status, ret = client.request("GET", url=url)

    if status == 200:
        ret=pd.DataFrame(ret['data'])

    return status, ret

def getFactor(group, key, *, factors=None,isymbol=None,stocks=None,startdate=None,enddate=None,period=None):
    """
    
    """
    if isymbol is None and stocks is None:
        return 400, {'detail': 'isymbol和stocks参数至少需要设置一个'}

    params=""

    if factors:
        if isinstance(factors,list):
            factors = ','.join(factors)
        params = f"{params}&fields={factors}"
    if isymbol:
        params = f"{params}&isymbol={isymbol}"
    if stocks:
        if isinstance(stocks, list):
            stocks = ','.join(stocks)
        params = f"{params}&stocks={stocks}"
    if startdate:
        params = f"{params}&startdate={startdate}"
    if enddate:
        params = f"{params}&enddate={enddate}"
    if period:
        params = f"{params}&period={period}"

    params = params[1:]

    url = f"/{group}/{key}?{params}"

    status, ret = client.request("GET", url=url)

    if status == 200:
        ret=pd.DataFrame(ret['data'])

    return status, ret

class FactorApiGenerator(object):
    def __build_list(self, group):
        def __list():
            return getList(group)
        
        return __list

    def __build_query(self,group):
        def __query(key, *, fields=None,isymbol=None,stocks=None,startdate=None,enddate=None,period=None):
            return getFactor( group, key, factors=fields, isymbol=isymbol,stocks=stocks,startdate=startdate,enddate=enddate,period=period)

        return __query

    def __build_api(self,group,api):
        def __api(*, fields=None,isymbol=None,stocks=None,startdate=None,enddate=None,period=None):
            return getFactor( group, api, factors=fields, isymbol=isymbol,stocks=stocks,startdate=startdate,enddate=enddate,period=period)

        return __api

    def __init__(self,group):
        self.__group = group
        self.__dict__["list"] = self.__build_list(group)
        self.__dict__["query"] = self.__build_query(group)

        status, retobjs = getList(group)
        if status == 200:
            for _, row in retobjs.iterrows():
                self.__dict__[row['key']] = self.__build_api(group, row['key'])
