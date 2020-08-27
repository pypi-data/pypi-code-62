#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='AlgorithmShare',
    version='0.0.6',
    author='zhangheng',
    author_email='270425473@qq.com',
    url='http://earthdataminer.casearth.cn',
    description='Intelligent Algorithm Share Framework',
    long_description=open('README.md').read(),
    packages=['AlgorithmShare'],
    install_requires=[
		'requests',
		'urllib3'
	]
)
