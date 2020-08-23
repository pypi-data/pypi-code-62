# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_dev']

package_data = \
{'': ['*']}

install_requires = \
['tomlkit>=0.7.0,<0.8.0', 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['poetry_dev = poetry_dev:app']}

setup_kwargs = {
    'name': 'poetry-dev',
    'version': '0.1.0',
    'description': 'A collection of scripts replace local packages with versions and vice versa',
    'long_description': None,
    'author': 'Marc Rijken',
    'author_email': 'marc@rijken.org',
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
