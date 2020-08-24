# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['opensubtitles_dataloader']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'numpy>=1.0,<2.0', 'torch>=1.0,<2.0', 'tqdm>=4.0,<5.0']

entry_points = \
{'console_scripts': ['opensubtitles-download = '
                     'opensubtitles_dataloader.__main__:download']}

setup_kwargs = {
    'name': 'opensubtitles-dataloader',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'Christoph Minixhofer',
    'author_email': 'christoph.minixhofer@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
