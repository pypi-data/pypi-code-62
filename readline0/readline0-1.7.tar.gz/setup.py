#!/usr/bin/env python3

"""Setup for readline0.py."""

from setuptools import setup


def get_readme():
    """Return the contents of README.rst as a string."""
    with open('README.rst', 'r') as file_:
        return file_.read()


setup(
    name="readline0",
    version="1.7",
    py_modules=['readline0'],

    # metadata for upload to PyPI
    author="Daniel Richard Stromberg",
    author_email="strombrg@gmail.com",
    description='Pure Python, relatively-efficient reading of null-terminated lines',
    long_description=get_readme(),
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
