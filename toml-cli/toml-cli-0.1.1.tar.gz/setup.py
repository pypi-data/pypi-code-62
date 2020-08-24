# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['toml_cli']

package_data = \
{'': ['*']}

install_requires = \
['tomlkit>=0.7.0,<0.8.0', 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['toml = toml_cli:main']}

setup_kwargs = {
    'name': 'toml-cli',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Marc Rijken',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
