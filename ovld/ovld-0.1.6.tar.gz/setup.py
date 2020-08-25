# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ovld']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ovld',
    'version': '0.1.6',
    'description': 'Overloading Python functions',
    'long_description': None,
    'author': 'Olivier Breuleux',
    'author_email': 'breuleux@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
