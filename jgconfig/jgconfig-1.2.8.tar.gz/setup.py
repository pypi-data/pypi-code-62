# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(name="jgconfig",
      description="jgconfig",
      version="1.2.8",
      author="jiegemena",
      author_email="jiegemena@outlook.com",
      packages=find_packages(),
      install_requires=[    # 依赖列表
          'requests',
          'pymysql',
          'redis'
      ]
    )
