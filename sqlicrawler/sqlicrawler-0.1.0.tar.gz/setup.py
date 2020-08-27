# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sqlicrawler']

package_data = \
{'': ['*']}

install_requires = \
['aiodns>=2.0.0,<3.0.0',
 'aiohttp>=3.6.2,<4.0.0',
 'aiohttp_socks>=0.5.3,<0.6.0',
 'click>=7.1.2,<8.0.0',
 'pyppeteer>=0.2.2,<0.3.0',
 'ujson>=3.1.0,<4.0.0']

entry_points = \
{'console_scripts': ['sqlicrawler = sqlicrawler:main']}

setup_kwargs = {
    'name': 'sqlicrawler',
    'version': '0.1.0',
    'description': 'SQLi Crawler with JavaScript support.',
    'long_description': None,
    'author': 'Sergey M',
    'author_email': 'tz4678@gmail.com',
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
