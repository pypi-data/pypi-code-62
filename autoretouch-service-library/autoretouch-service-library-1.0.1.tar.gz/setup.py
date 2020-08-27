# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['autoretouchlib']

package_data = \
{'': ['*']}

install_requires = \
['autopep8>=1.5.4,<2.0.0',
 'canonicaljson>=1.3.0,<2.0.0',
 'fakeredis>=1.4.3,<2.0.0',
 'fastapi>=0.61.0,<0.62.0',
 'redis>=3.5.3,<4.0.0',
 'requests_mock>=1.8.0,<2.0.0']

setup_kwargs = {
    'name': 'autoretouch-service-library',
    'version': '1.0.1',
    'description': 'Autoretouch helper library',
    'long_description': None,
    'author': 'Nicolas Dieumegarde',
    'author_email': 'nicolas.dieumegarde@cmdscale.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
