# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pykir']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pykir',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'Kiran PS',
    'author_email': 'kiran.ps@shuttl.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
