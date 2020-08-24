#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : errcode.py
# @Author: encircles
# @Date  : 8/19/2020
# @Desc  :

SUCCESS = 0
UNKNOWN = 10000

# Tencent
TX_ID_IS_NONE = 20000  # secret id is None
TX_KEY_IS_NONE = 20001  # secret key is None
TX_REGION_NONE = 20002  # region is None
TX_ENDPOINT_NONE = 20003  # endpoint is None

# Ali
AL_ID_IS_NONE = 30000  # access key id is None
AL_SECRET_IS_NONE = 30001  # access key secret is None

errmsg = {
    0: "success",
    10000: "未知错误",

    # Tencent
    20000: "secret id is None",
    20001: "secret key is None",
    20002: "region is None",
    20003: "endpoint is None",

    # Ali
    30000: "access key id is None",
    30001: "access key secret is None",
}


def getErrMsg(code):
    return errmsg.get(code)
