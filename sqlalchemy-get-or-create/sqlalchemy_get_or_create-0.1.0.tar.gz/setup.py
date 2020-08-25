# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sqlalchemy_get_or_create']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sqlalchemy-get-or-create',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Enrico Barzetti',
    'author_email': 'enricobarzetti@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
