# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zotero_sync']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'python-dotenv>=0.14.0,<0.15.0',
 'requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'zotero-sync',
    'version': '0.1.0',
    'description': 'A module for managing zotfiles',
    'long_description': None,
    'author': 'Jacob Clarke',
    'author_email': 'jacobclarke718@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
