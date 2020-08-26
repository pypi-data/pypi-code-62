#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Zheng <zxyful@gmail.com>
# Date: 2019/7/25
# Desc: 

from urllib.parse import urlparse, unquote


def parse_params(params_url):
    """

    :param params_url:
    :return:
    """
    params = dict()
    if not params_url:
        return params

    items = params_url.split('&')
    for param in items:
        k, v = param.split('=')
        if v.isnumeric():
            v = int(v)
        else:
            v = unquote(v)
        params.update({k: v})
    return params


class UriParser:
    # <scheme>://<user>:<pwd>@<host>:<port>/<path>;<params>?<query>#<frag>
    def __init__(self, uri):
        self.handle = urlparse(uri)

    @property
    def scheme(self):
        return self.handle.scheme

    @property
    def user(self):
        return self.handle.username

    @property
    def password(self):
        return self.handle.password

    @property
    def host(self):
        return self.handle.hostname

    @property
    def port(self):
        return self.handle.port

    @property
    def db(self):
        path = self.handle.path
        return path.replace("/", "")

    @property
    def params(self):
        return parse_params(self.handle.query)

    @property
    def fragment(self):
        return self.handle.fragment

    def __repr__(self):
        return "URI:{}:{}".format(self.host, self.port)
