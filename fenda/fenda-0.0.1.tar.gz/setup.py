# -*- coding: utf-8 -*-
import setuptools

import legato 

with open("README.md") as f:
    long_description = f.read()

setuptools.setup(
    name="fenda",
    version=legato.__version__,
    author="rejown",
    author_email="rejown@gmail.com",
    description="A WSGI Server Implementation of OpenAPI 3.0 in Python3.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://fenda.io/ff/legato",
    packages=['legato'],
    python_requires='>=3.6',
    install_requires=[
        'jsonschema',
    ],
    tests_require=[
        'pytest',
    ],
)
