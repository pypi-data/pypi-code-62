# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wscrap']

package_data = \
{'': ['*']}

install_requires = \
['aiodns>=2.0.0,<3.0.0',
 'aiohttp>=3.6.2,<4.0.0',
 'beautifulsoup4>=4.9.1,<5.0.0',
 'lxml>=4.5.2,<5.0.0']

entry_points = \
{'console_scripts': ['wscrap = wscrap:main']}

setup_kwargs = {
    'name': 'wscrap',
    'version': '0.1.0',
    'description': 'Command line web scrapping tool',
    'long_description': '# WScrap\n\nCommand line web scrapping tool.\n\nUsage:\n\n```zsh\n$ pip install wscrap\n# The output format is JSONL. Use jq to parse it.\n$ wscrap -i domain_list.txt -o resutls.json -vv 2> log.txt\n\n# or without install\n$ pipx run wscrap -h\n```\n',
    'author': 'Sergey M',
    'author_email': 'tz4678@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tz4678/wscrap',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
