# -*-coding:utf-8-*-
"""
@Author: LinGuilin
@Date: 2020-08-21 14:07:08
@LastEditTime: 2020-08-24 16:54:17
@LastEditors: ChenXiaolei
@Description: 企业微信消息发送类和企业微信授权登录类

"""

from seven_framework.sign import SignHelper
import time
import requests


class OauthHelper(object):
    """"
    @description:企业微信认证登录生成链接类
    Usage::

      >>> from seven_framework import *
      >>> oauth = OauthHelper(app_id=APP_ID,app_key=APP_KEY)
      >>> res = oauth.get_web_auth_link(redirect_uri='https://httpbin.org/get',state=STATE)
      >>> if res:
      >>>       print('res)
      https://open.weixin.qq.com/connect/oauth2/...
    """

    def __init__(self, app_id, app_key, url=None):
        """
        @description: 初始化参数
        @param app_id: 应用id
        @param app_key: 应用凭证
        @param url: 请求路径
        @last_editors: LinGuilin
        """

        self.url = url
        if not url or url == "":
            self.url = "https://wwc.gao7.com/api/auth/get_link"

        self.app_key = app_key
        self.app_id = app_id

    def _get_request_params(self, redirect_uri, link_type, state=None,):
        """
        @description: 
        @param redirect_uri:重定向链接
        @param state: 透传参数
        @param link_type: 链接类型 code/web
        @return dict  请求参数字典 
        @last_editors: LinGuilin
        """
        timestamp = int(time.time())
        params = {}
        params["timestamp"] = timestamp
        params["redirect_uri"] = redirect_uri
        params["state"] = state
        params["link_type"] = link_type
        params["app_id"] = self.app_id

        # 生成签名
        sign = SignHelper.params_sign_md5(params=params, app_key=self.app_key)
        # 构造请求参数
        params["sign"] = sign
        return params

    def get_web_auth_link(self, redirect_uri, state=None):
        """
        @description: 获取网页认证登录链接
        @param redirect_uri: 重定向链接 
        @param state: 透传参数
        @return 链接或者None
        @last_editors: LinGuilin
        """

        params = self._get_request_params(
            redirect_uri=redirect_uri, state=state, link_type="web")
        try:
            res = requests.get(url=self.url, params=params).json()
            if int(res["result"]) == 1:
                return res["data"]["auth_url"]
            print(f"get请求url:{self.url}异常,{res['desc']}")
            return None
        except:
            print(f"get请求url:{self.url},params:{params}异常")
            return None

    def get_code_auth_link(self, redirect_uri, state=None):
        """
        @description: 获取二维码认证登录链接
        @param redirect_uri: 重定向链接 
        @param state: 透传参数
        @return 链接或者None
        @last_editors: LinGuilin
        """

        params = self._get_request_params(
            redirect_uri=redirect_uri, state=state, link_type="code")

        try:
            res = requests.get(url=self.url, params=params).json()
            if int(res["result"]) == 1:
                return res["data"]["auth_url"]
            print(f"get请求url:{self.url}异常,{res['desc']}")
            return None
        except:
            print(f"get请求url:{self.url},params:{params}异常")
            return None


class MessageHelper(object):
    """"
    @description:企业微信消息发送类
    Usage::

      >>> from seven_framework import *
      >>> msg = MessageHelper(app_id=APP_ID,app_key=APP_KEY)
      >>> res = msg.send_msg_by_account(notice_object='1234',notice_content='test message')
      >>> if res:
      >>>       print('success')
      success
    """

    def __init__(self, app_id, app_key, url=None):
        """
        @description: 初始化参数
        @param app_id: 应用id
        @param url: 请求的url
        @param app_key: 应用凭证
        @last_editors: LinGuilin
        """
        self.url = url
        if not url or url == "":
            self.url = "https://wwc.gao7.com/api/message/send"

        self.app_key = app_key
        self.app_id = app_id

    def _get_request_params(self, notice_content, notice_object, notice_object_type, notice_content_type="text"):
        """
        @description: 获取请求参数
        @param notice_content: 消息内容
        @param notice_content_type: 消息内容类型
        @param notice_object: 消息接收对象
        @param notice_object_type: 消息接收对象类型
        @return dict  消息字典
        @last_editors: LinGuilin
        """

        timestamp = int(time.time())
        params = {}
        params["app_id"] = self.app_id
        params["timestamp"] = timestamp
        params["notice_object_type"] = notice_object_type
        params["notice_content"] = notice_content
        params["notice_content_type"] = notice_content_type
        params["notice_object"] = notice_object

        # 生成签名
        sign = SignHelper.params_sign_md5(params=params, app_key=self.app_key)

        # 构建请求字典
        params["sign"] = sign
        return params

    def send_msg_by_webhook(self, notice_content, notice_object, notice_content_type="text"):
        """
        @description: 发送机器人消息
        @param notice_content:消息内容
        @param notice_content_type：消息内容类型
        @param notice_object：消息接收对象
        @return 成功为True 失败 None
        @last_editors: LinGuilin
        """

        params = self._get_request_params(
            notice_content=notice_content, notice_content_type=notice_content_type, notice_object=notice_object, notice_object_type="webhook")

        try:
            res = requests.post(url=self.url, data=params, headers={
                                'Content-Type': 'application/x-www-form-urlencoded'}).json()
            if int(res["result"]) == 1:
                return True
            print(f"post请求url:{self.url}异常,{res['desc']}")
            return None
        except:
            print(f"post请求url:{self.url},params:{params}异常")
            return None

    def send_msg_by_template(self, notice_content, notice_object, notice_content_type="text"):
        """
        @description: 发送模板消息
        @param notice_content: 消息内容
        @param notice_content_type: 消息内容类型
        @param notice_object: 消息接收对象
        @return 成功为True 失败 None
        @last_editors: LinGuilin
        """

        params = self._get_request_params(notice_content=notice_content, notice_content_type=notice_content_type,
                                          notice_object=notice_object, notice_object_type="template")
        try:
            res = requests.post(url=self.url, data=params, headers={
                                'Content-Type': 'application/x-www-form-urlencoded'}).json()
            if int(res["result"]) == 1:
                return True
            print(f"post请求url:{self.url}异常,{res['desc']}")
            return None
        except:
            print(f"post请求url:{self.url},params:{params}异常")
            return None

    def send_msg_by_account(self, notice_content, notice_object, notice_content_type="text"):
        """
         @description: 发送微信用户消息
         @param notice_content: 消息内容
         @param notice_content_type: 消息内容类型
         @param notice_object: 消息接收对象
         @return 成功为True 失败 None
         @last_editors: LinGuilin
         """

        params = self._get_request_params(
            notice_content=notice_content, notice_content_type=notice_content_type, notice_object=notice_object, notice_object_type="account")

        try:
            res = requests.post(url=self.url, data=params, headers={
                                'Content-Type': 'application/x-www-form-urlencoded'}).json()
            if int(res["result"]) == 1:
                return True
            print(f"post请求url:{self.url}异常,{res['desc']}")
            return None
        except:
            print(f"post请求url:{self.url},params:{params}异常")
            return


