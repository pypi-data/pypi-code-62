# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bella', 'bella.modules']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'bella',
    'version': '2.1.3',
    'description': 'BellaPy - A useful helper for any python program',
    'long_description': None,
    'author': 'Dong Nguyen',
    'author_email': 'ndaidong@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
