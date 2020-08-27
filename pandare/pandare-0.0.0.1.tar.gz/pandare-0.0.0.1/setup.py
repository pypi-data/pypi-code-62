#! /usr/bin/env python

from __future__ import print_function
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import io
import os
import sys

long_description = """
This is a dummy package for future use. See website.
"""


setup(
    name='pandare',
    version="0.0.0.1",
    url='http://github.com/panda-re/panda/',
    license='GPLv2',
    author='panda-re',
    tests_require=[],
    install_requires=[],
    cmdclass={},
    author_email='luke@lukecraig.com',
    description='Dummy package for later use with python panda',
    long_description=long_description,
    include_package_data=True,
    platforms='any',
    test_suite='',
    classifiers = [
        'Programming Language :: Python',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    #zip_safe = True,
)
