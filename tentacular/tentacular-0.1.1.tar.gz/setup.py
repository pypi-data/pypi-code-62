# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tentacular']

package_data = \
{'': ['*']}

install_requires = \
['starlette>=0.13.8,<0.14.0', 'uvicorn>=0.11.8,<0.12.0']

setup_kwargs = {
    'name': 'tentacular',
    'version': '0.1.1',
    'description': 'M5Stack IoT Edge',
    'long_description': None,
    'author': 'Mihails Delmans',
    'author_email': 'm.delmans@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
