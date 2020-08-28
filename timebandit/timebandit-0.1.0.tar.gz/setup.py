# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['timebandit']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.5.1,<0.6.0', 'wheel>=0.35.1,<0.36.0']

setup_kwargs = {
    'name': 'timebandit',
    'version': '0.1.0',
    'description': 'The most fabulous time measuring object in the world.',
    'long_description': None,
    'author': 'skeptycal',
    'author_email': '26148512+skeptycal@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
