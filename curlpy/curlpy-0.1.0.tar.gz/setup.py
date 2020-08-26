# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['curlpy']
setup_kwargs = {
    'name': 'curlpy',
    'version': '0.1.0',
    'description': 'curl like python interface',
    'long_description': None,
    'author': 'ucpr',
    'author_email': 'contact@ucpr.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
