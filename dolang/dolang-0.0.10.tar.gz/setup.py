# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dolang', 'dolang.tests']

package_data = \
{'': ['*']}

install_requires = \
['lark-parser>=0.9.0,<0.10.0',
 'numba>=0.50',
 'numpy>=1.18.3,<2.0.0',
 'sympy>=1.5.1,<2.0.0']

setup_kwargs = {
    'name': 'dolang',
    'version': '0.0.10',
    'description': 'Dolo Modeling Language',
    'long_description': '# dolang.py\n\nVery empty README file.\n',
    'author': 'Winant Pablo',
    'author_email': 'pablo.winant@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
