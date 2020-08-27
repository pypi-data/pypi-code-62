# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ecis_processing']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.0.5,<2.0.0']

entry_points = \
{'console_scripts': ['ecis-processing = ecis_processing.__main__:main']}

setup_kwargs = {
    'name': 'ecis-processing',
    'version': '0.5.0',
    'description': 'A program that processes diagnosis and medication data ',
    'long_description': "ECIS Data Processing\n=====================\n\n.. code-block::\n\n    usage: ecis-processing [-h] [-o OUTPUT] DIRECTORY\n\n    Process diagnosis and medication data.\n\n    positional arguments:\n      DIRECTORY             path to input directory\n\n    optional arguments:\n      -h, --help            show this help message and exit\n      -o OUTPUT, --output OUTPUT\n                            output file name, defaults to 'processed.csv'\n\n\n",
    'author': 'Fisher Sun',
    'author_email': 'fisher521.fs@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tactlessfish/ecis-processing',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
