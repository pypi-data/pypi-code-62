#!/usr/bin/env python3

"""Setup for readline0.py."""

from setuptools import setup

setup(
    name="readline0",
    version="1.2",
    py_modules=['readline0'],

    # metadata for upload to PyPI
    author="Daniel Richard Stromberg",
    author_email="strombrg@gmail.com",
    description='Pure Python, relatively-efficient reading of null-terminated lines',
    long_description='''
Read lines of data with an arbitrary delimiter, like a null, newline or x.

It passes pylint, passes pycodestyle, passes pydocstyle, is thoroughly unit tested, and runs on CPython 2.7, CPython 3.x,
Pypy 7.3.1, Pypy3 7.3.1.

It gains a lot of speed by eschewing single-character reads.
''',
    license="UCI, from UC Regents",
    keywords="text lines delimiter",
    url='https://stromberg.dnsalias.org/~strombrg/readline0.html',
    platforms='Cross platform',
    classifiers=[
         "Development Status :: 5 - Production/Stable",
         "Intended Audience :: Developers",
         "Programming Language :: Python :: 2",
         "Programming Language :: Python :: 3",
         ],
)
