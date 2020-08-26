#!/usr/bin/env python3

"""Setup for readline0.py."""

from setuptools import setup

setup(
    name="readline0",
    version="1.4",
    py_modules=['readline0'],

    # metadata for upload to PyPI
    author="Daniel Richard Stromberg",
    author_email="strombrg@gmail.com",
    description='Pure Python, relatively-efficient reading of null-terminated lines',
    long_description_content_type='text/plain',
    long_description='''
Read lines of data with an arbitrary delimiter, like a null, newline or even an x.

It passes pylint, passes pycodestyle, passes pydocstyle, is thoroughly unit tested, and runs on CPython 2.7, CPython 3.x,
Pypy 7.3.1, Pypy3 7.3.1.

It gains a lot of speed by eschewing single-character reads.

Usage looks like:
    $ /usr/local/cpython-3.6/bin/python3
    Python 3.6.0 (default, Apr 22 2017, 09:17:19)
    [GCC 5.4.0 20160609] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import readline0
    >>> file_ = open('/etc/shells', 'r')
    >>> for line in readline0.readline0(file_=file_, separator=b'\n'):
    ...     print(line)
    ...
    b'# /etc/shells: valid login shells'
    b'/bin/sh'
    b'/bin/dash'
    b'/bin/bash'
    b'/bin/rbash'
    >>>

Of course separator need not be a newline; it defaults to a null byte.
Also file_ defaults to sys.stdin.
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
