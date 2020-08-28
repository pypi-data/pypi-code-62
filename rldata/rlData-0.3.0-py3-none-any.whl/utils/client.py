#coding:utf-8
'''
# File Name: client.py
# Author: joyle
# mail: joyle.zhang@qq.com
# Created Time: 2020年08月03日 星期一 00时00分00秒
'''
import os
import urllib
import json
from passlib.context import CryptContext

__all__ = [
    "client",
    "login",
]

BASE_URL = os.getenv("RLDATA_URL","http://121.37.138.1:8000/RlData")
DEFAULT_VERSION = os.getenv("RLDATA_VERSION","v1")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Client(object):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__( self, *, url=BASE_URL, apiVersion=DEFAULT_VERSION):
        self.baseUrl=url
        self.apiUrl = f"{url}/{apiVersion}"
        self.token=None

    def __call__( self, *, url=BASE_URL, apiVersion=DEFAULT_VERSION):
        self.baseUrl=url
        self.apiUrl = f"{url}/{apiVersion}"
        self.token=None

    @classmethod
    def _req( cls, method, url, body, header ):
        req = urllib.request.Request(url=url,data=body,headers=header,method=method)
        try:
            res = urllib.request.urlopen(req)
            return res.status, json.loads(res.read())
        except urllib.error.HTTPError as e:
            if e.code == 307:
                return cls._req( method, e.hdrs['location'], body, header )
            else:
                return e.code, {"detail":e.msg}

    def request( self, method, url, body=None, headers={"accept": "application/json"} ):
        retobj = None
        if self.token:
            headers.update({"Authorization": f"{self.token['token_type']} {self.token['access_token']}"})

        status, retobj = self._req( method, f"{self.apiUrl}{url}", body, headers )

        if self.token and "access_token" in retobj.keys():
            self.token["access_token"] = retobj["access_token"]
            del retobj["access_token"]

        return status, retobj

    def login(self, username, password ):
        """ 
        
        """
        params = urllib.parse.urlencode(dict({'username': username, 'password': pwd_context.hash(password)}))
        header = {
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        data = bytes(params, encoding='utf8')

        status, retobj = self._req( "POST", f'{self.baseUrl}/token', data, header )
        if status == 200:
            self.token=retobj

        return status, retobj

client=Client()

def login(username,password):
    return client.login(username,password)

if __name__ == '__main__':
    a = Client()
    s, ret = a.request("GET", "/factor/daily_price?stocks=300012,600519")
    print(ret)
    s, ret = a.login("joyle","j0y138oe")
    print(ret)
    s, ret = a.request("GET", "/factor/daily_price?stocks=300012,600519")
    print(ret)
