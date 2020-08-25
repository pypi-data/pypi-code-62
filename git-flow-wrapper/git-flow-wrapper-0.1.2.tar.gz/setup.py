# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['git_flow_wrapper']

package_data = \
{'': ['*']}

install_requires = \
['typer>=0.1.0,<0.2.0']

entry_points = \
{'console_scripts': ['flow = git_flow_wrapper.cli:main']}

setup_kwargs = {
    'name': 'git-flow-wrapper',
    'version': '0.1.2',
    'description': 'Wrapper to run common git flow commands with remote repositories',
    'long_description': None,
    'author': 'Patrick',
    'author_email': 'patrick.pwall@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
