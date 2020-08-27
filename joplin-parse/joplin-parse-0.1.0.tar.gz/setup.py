# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['joplin_parse']

package_data = \
{'': ['*']}

install_requires = \
['asyncio>=3.4.3,<4.0.0', 'joplin-api>=1.5.6,<2.0.0', 'wrapt>=1.12.1,<2.0.0']

setup_kwargs = {
    'name': 'joplin-parse',
    'version': '0.1.0',
    'description': 'Turn Joplin database into public wiki',
    'long_description': None,
    'author': 'Rasul Kireev',
    'author_email': 'me@rasulkireev.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
