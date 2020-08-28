# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['imgavg']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.1,<2.0.0', 'pillow>=7.2.0,<8.0.0']

entry_points = \
{'console_scripts': ['imgavg = imgavg.cli:main']}

setup_kwargs = {
    'name': 'imgavg',
    'version': '0.6',
    'description': 'A command line utility that outputs the average of a number of pictures.',
    'long_description': None,
    'author': 'Joeseph Rodrigues',
    'author_email': 'dowhilegeek@gmail.com',
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
