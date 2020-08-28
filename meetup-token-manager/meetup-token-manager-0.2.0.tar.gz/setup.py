# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['meetup', 'meetup.token_manager']

package_data = \
{'': ['*']}

install_requires = \
['google-cloud-storage>=1.31.0,<2.0.0',
 'ipykernel>=5.3.4,<6.0.0',
 'object-storage>=0.14.2,<0.15.0',
 'pylint>=2.6.0,<3.0.0',
 'redis>=3.3,<4.0',
 'requests>=2.22,<3.0']

setup_kwargs = {
    'name': 'meetup-token-manager',
    'version': '0.2.0',
    'description': 'Easily obtain and cache OAuth 2.0 token from the Meetup API.',
    'long_description': None,
    'author': 'Jan-Benedikt Jagusch',
    'author_email': 'jan.jagusch@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/janjagusch/meetup-token-manager',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
