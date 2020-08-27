#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

import remove_cookies_notice

setup(
    name="remove_cookies_notice",
    version=remove_cookies_notice.__version__,
    packages=find_packages(),
    author="Laurent Evrard",
    author_email="laurent@owlint.fr",
    description="Tool to remove cookies notice in html pages",
    long_description=open("README.md").read(),
    install_requires=[],
    url="https://github.com/owlint/CookiesNoticeRemover",
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 1 - Planning",
        "License :: OSI Approved",
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Topic :: Communications",
    ],
    license="WTFPL",
)
