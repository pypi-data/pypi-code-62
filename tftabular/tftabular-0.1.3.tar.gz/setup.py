# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tftabular']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.1,<2.0.0',
 'pandas>=0.25.1',
 'pendulum>=2.1.2,<3.0.0',
 'tensorflow>=2.2.0,<3.0.0',
 'tensorflow_addons>=0.11.1,<0.12.0']

setup_kwargs = {
    'name': 'tftabular',
    'version': '0.1.3',
    'description': 'A flexible implementation of [TabNet](https://arxiv.org/pdf/1908.07442.pdf) in Tensorflow 2.0',
    'long_description': None,
    'author': 'marcusinthesky',
    'author_email': 'gwrmar002@myuct.ac.za',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
