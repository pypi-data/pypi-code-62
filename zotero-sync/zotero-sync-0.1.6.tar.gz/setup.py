# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zotero_sync']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'ocrmypdf>=11.0.1,<12.0.0',
 'python-dotenv>=0.14.0,<0.15.0',
 'requests>=2.24.0,<3.0.0']

entry_points = \
{'console_scripts': ['zotero_sync = zotero_sync.__main__:cli']}

setup_kwargs = {
    'name': 'zotero-sync',
    'version': '0.1.6',
    'description': 'A module for managing zotfiles files',
    'long_description': '# Zotero Sync\n\n![demo](demo.gif)\n\n`Back up your data when using this script. I have not lost any, but I can\'t make any guarantees.`\n\nA simple module for updating zotflies directories. You can use this to delete redundant files or upload newly added files from the filesystem. It works by looking at every reference you have on zotero.org (you don\'t need to have files uploaded to make this work) and then compares the paths of those attachements to the ones in you zotfile directory. If there are any on your zotfile directory that aren\'t in your zotfile cloud, you can choose to "trash" or "upload" them.\n\n## Installation\n\n```zsh\npip install zotero_sync\n```\n\n## Usage\n\nGo and create a new api key at https://www.zotero.org/settings/keys. Take note of the api key and also take note of the line that says "Your userID for use in API calls is ***"\n\nCreate a `.zoterosync` file in your home directory:\n\n``` json\n# ~/.zoterosync\n\nZOTFILE_DIR=\'***\'\nUSER_ID = \'***\'\nAPI_KEY = \'***\'\n```\n\nFor information on script usage.\n\n```zsh\nzotero_sync --help\n```\n\n',
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
