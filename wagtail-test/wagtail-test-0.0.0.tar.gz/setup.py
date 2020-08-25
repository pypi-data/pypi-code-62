#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name="wagtail-test",
    install_requires=["Django>=3.1,<3.2", "wagtail>=2.10,<2.11",],
    packages=["home", "mysite", "search", "home.migrations", "mysite.settings",],
    py_modules=["manage",],
)
