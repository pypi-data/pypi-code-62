#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : client.py
# @Author: encircles
# @Date  : 8/19/2020
# @Desc  :
import json
import sys

import decouple

from srvmsdk.SrvmException import SrvmException
from srvmsdk.common import errcode
from srvmsdk.common.commonbase import CommonBase
from srvmsdk.common.aliyun.aliclient import AliClient
from srvmsdk.common.tencent.txclient import TxClient


def get_client(client_type, **kwargs):
    client_type = client_type.lower()
    if client_type == "tencent":
        return TxClient(kwargs.get('secret_id'), kwargs.get('secret_key'), kwargs.get('region'))
    elif client_type == "aliyun":
        return AliClient(kwargs.get('access_key_id'), kwargs.get('access_key_secret'))
    else:
        raise SrvmException('-1', 'err')


if __name__ == '__main__':
    # sys.exit()
    sid = decouple.config('S_ID')
    skey = decouple.config('S_KEY')
    region = decouple.config('REGION')

    params = '{}'

    tencent = get_client('tencent', secret_id=sid, secret_key=skey, region=region)
    res = tencent.RunInstances(params)

    print(res.get('code'))
    print(json.dumps(res, ensure_ascii=False))
