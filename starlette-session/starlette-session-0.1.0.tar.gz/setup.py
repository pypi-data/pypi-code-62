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
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Aurélien Dentan',
    'author_email': 'aurelien.dentan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
