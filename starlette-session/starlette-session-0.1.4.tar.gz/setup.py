# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['starlette_session']

package_data = \
{'': ['*']}

install_requires = \
['itsdangerous>=1.1.0,<2.0.0', 'starlette>=0.13.8,<0.14.0']

setup_kwargs = {
    'name': 'starlette-session',
    'version': '0.1.4',
    'description': 'A library for backend side session with starlette',
    'long_description': '# Starlette Session\n\n<p align="center">\n\n<a href="https://github.com/auredentan/starlette-session/actions?query=workflow%3ATest" target="_blank">\n    <img src="https://github.com/auredentan/starlette-session/workflows/Test/badge.svg?branch=master" alt="Test">\n</a>\n\n<a href="https://pypi.org/project/starlette-session" target="_blank">\n    <img src="https://img.shields.io/pypi/v/starlette-session?color=%2334D058&label=pypi%20package" alt="Package version">\n</a>\n\n<a href="https://codecov.io/gh/auredentan/starlette-session">\n  <img src="https://codecov.io/gh/auredentan/starlette-session/branch/master/graph/badge.svg" />\n</a>\n\n</p>\n\n---\n\nStarlette session middleware',
    'author': 'Aurélien Dentan',
    'author_email': 'aurelien.dentan@gmail.com',
    'maintainer': 'Aurélien Dentan',
    'maintainer_email': 'aurelien.dentan@gmail.com',
    'url': 'https://github.com/auredentan/starlette-sessionhttps://github.com/auredentan/starlette-session',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
