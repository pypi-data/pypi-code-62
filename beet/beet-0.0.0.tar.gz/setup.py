# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['beet']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['beet = beet.cli:main']}

setup_kwargs = {
    'name': 'beet',
    'version': '0.0.0',
    'description': 'A python library and toolchain for programmatic Minecraft data packs and resource packs',
    'long_description': '# beet\n\n> A python library and toolchain for programmatic Minecraft data packs and resource packs.\n\n---\n\nLicense - [MIT](https://github.com/vberlier/beet/blob/master/LICENSE)\n',
    'author': 'Valentin Berlier',
    'author_email': 'berlier.v@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vberlier/beet',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
