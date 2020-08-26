# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tinycardl']

package_data = \
{'': ['*']}

install_requires = \
['aiocsv>=1.1.0,<2.0.0',
 'aiofiles>=0.5.0,<0.6.0',
 'aioify>=0.3.2,<0.4.0',
 'httpx-auth>=0.5.0,<0.6.0',
 'httpx>=0.14.1,<0.15.0',
 'python-jose>=3.2.0,<4.0.0']

entry_points = \
{'console_scripts': ['tinycardl = tinycardl:main.entrypoint']}

setup_kwargs = {
    'name': 'tinycardl',
    'version': '1.0.0',
    'description': 'Download your cards',
    'long_description': '# Tinycardl\n\n**_Tinycards downloader_**\n\nTinycardl downloads decks, deck groups and your pinned in CSV, along with the pictures.\n\n🚧 This is a work in progress which will never be finished, but I hope it will be useful for some of you.\n\n### Usage\n\nInstallation:\n\n`python3.8 -m pip install --user tinycardl`\n\nBasic usage, downloading decks or deck groups:\n\n`tinycardl 3AbdmJDP NZHWAf`\n\nTo download you pinned decks, you need you JWT token.\nOnce logged in Tinycard with your Duolingo account, look for the cookie `jwt_token` in the Development Tools of your browser (press F12).  \n- For Chrome it’s under **Application > Cookies > https://tinycards.duolingo.com > jwt_token > Value**  \n- For Firefox it’s under **Storage > Cookies > https://tinycards.duolingo.com > jwt_token > Value**  \n\n`JWT_TOKEN=myVery.l0ng.t0k3n tinycardl`\n\n',
    'author': 'Baptiste Darthenay',
    'author_email': 'baptiste.darthenay@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/batisteo/tinycardl',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
