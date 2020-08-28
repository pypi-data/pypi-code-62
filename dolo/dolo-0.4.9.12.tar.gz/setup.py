# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dolo',
 'dolo.algos',
 'dolo.compiler',
 'dolo.misc',
 'dolo.numeric',
 'dolo.numeric.discretization',
 'dolo.numeric.extern',
 'dolo.numeric.optimize',
 'dolo.tests']

package_data = \
{'': ['*']}

install_requires = \
['dolang>=0.0.10,<0.0.11',
 'interpolation>=2.1.6,<3.0.0',
 'ipython>=7.13.0,<8.0.0',
 'matplotlib>=3.0.1,<4.0.0',
 'multipledispatch>=0.6.0,<0.7.0',
 'numpy>=1.16.0,<2.0.0',
 'pandas>=1.0.3,<2.0.0',
 'pyyaml>=5.3.1,<6.0.0',
 'quantecon>=0.4.7,<0.5.0',
 'ruamel.yaml>=0.16.10,<0.17.0',
 'scipy>=1.4.1,<2.0.0',
 'xarray>=0.15.1,<0.16.0']

setup_kwargs = {
    'name': 'dolo',
    'version': '0.4.9.12',
    'description': 'Economic Modeling in Python',
    'long_description': 'Complete documentation with installation instruction, available at http://dolo.readthedocs.org/en/latest/\n\nJoin the chat at https://gitter.im/EconForge/dolo\n\n[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/EconForge/dolo.git/master?urlpath=lab)\n',
    'author': 'Winant Pablo',
    'author_email': 'pablo.winant@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
