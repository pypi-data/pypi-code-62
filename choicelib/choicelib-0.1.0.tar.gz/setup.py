# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['choicelib']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'choicelib',
    'version': '0.1.0',
    'description': 'Choice a best similar-interface library from given list',
    'long_description': None,
    'author': 'timoniq',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
