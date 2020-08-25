# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['klusterinfo']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0', 'pint>=0.9.0,<0.10.0', 'pykubeks==0.1.0']

entry_points = \
{'console_scripts': ['klusterinfo = klusterinfo:cli']}

setup_kwargs = {
    'name': 'klusterinfo',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Steinn Eldjárn Sigurðarson',
    'author_email': 'steinnes@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
