# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['autosys',
 'autosys.cli',
 'autosys.cli.colors',
 'autosys.debug',
 'autosys.examples',
 'autosys.exceptions',
 'autosys.implore',
 'autosys.log',
 'autosys.math_utils',
 'autosys.parse',
 'autosys.parse.sample_data',
 'autosys.profile',
 'autosys.text_utils',
 'autosys.twitter',
 'autosys.utils',
 'autosys.web',
 'autosys.web.google',
 'autosys.web.json',
 'autosys.web.medium',
 'autosys.web.webpages']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'colorama>=0.4.3,<0.5.0',
 'requests>=2.24.0,<3.0.0',
 'toml>=0.10.1,<0.11.0']

setup_kwargs = {
    'name': 'autosys',
    'version': '0.5.0',
    'description': 'System Utilities for Python on macOS.',
    'long_description': None,
    'author': 'skeptycal',
    'author_email': '26148512+skeptycal@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
