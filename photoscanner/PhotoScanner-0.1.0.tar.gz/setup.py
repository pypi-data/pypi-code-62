# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['photoscanner']

package_data = \
{'': ['*']}

install_requires = \
['argparse>=1.4.0,<2.0.0',
 'imutils>=0.5.3,<0.6.0',
 'numpy>=1.19.1,<2.0.0',
 'opencv-python>=4.4.0,<5.0.0']

entry_points = \
{'console_scripts': ['photoscanner = photoscanner.main:run']}

setup_kwargs = {
    'name': 'photoscanner',
    'version': '0.1.0',
    'description': 'A simple tool to digitalize printed photos using a greenscreen and a DSLR.',
    'long_description': None,
    'author': 'Florian Vahl',
    'author_email': 'florian@flova.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
