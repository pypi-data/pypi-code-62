#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : setup.py
# @Author: encircles
# @Date  : 8/18/2020
# @Desc  :
from setuptools import setup, find_packages

setup(
    name="srvmsdk",
    version="0.0.8",
    url="https://github.com/encircles/srvmsdk",
    long_description=open('README.md').read(),
    packages=find_packages(),
    install_requires=['tencentcloud-sdk-python', 'decouple'],
)

'''
name 包的名字
version 依赖关系很重要
packages 需要包含的子包列表，用find_packages()查找
url：包的链接，通常为 Github 上的链接，或者是 readthedocs 链接
setup_requires：指定依赖项
test_suite：测试时运行的工具
'''
