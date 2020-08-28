# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['monologue', 'monologue.migrations']

package_data = \
{'': ['*'], 'monologue': ['static/*', 'templates/*']}

install_requires = \
['django>=3.0.8,<4.0.0', 'markdown>=3.2.2,<4.0.0']

setup_kwargs = {
    'name': 'django-monologue',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'An Long',
    'author_email': 'aisk1988@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
