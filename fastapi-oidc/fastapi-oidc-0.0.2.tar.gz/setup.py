# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_oidc']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.61.0,<0.62.0']

setup_kwargs = {
    'name': 'fastapi-oidc',
    'version': '0.0.2',
    'description': 'A simple library for parsing and verifying externally issued OIDC ID tokens in fastapi.',
    'long_description': None,
    'author': 'HarryMWinters',
    'author_email': 'harrymcwinters@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
