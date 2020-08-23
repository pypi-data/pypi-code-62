# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zotero_sync']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'python-dotenv>=0.14.0,<0.15.0',
 'requests>=2.24.0,<3.0.0']

entry_points = \
{'console_scripts': ['zotero_sync = src.__main__:cli']}

setup_kwargs = {
    'name': 'zotero-sync',
    'version': '0.1.3',
    'description': 'A module for managing zotfiles files',
    'long_description': '# Zotero Sync\n\nA simple module for updating zotflies directories.\n\n## Installation\n\n```zsh\npip install zotero_sync\n```\n\n## Usage\n\n```zsh\npython -m zotero_sync --help\n```',
    'author': 'Jacob Clarke',
    'author_email': 'jacobclarke718@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://jacobclarke.live/zotero-sync/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
