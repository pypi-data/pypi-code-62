# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['paperoni']

package_data = \
{'': ['*'], 'paperoni': ['commands/*']}

install_requires = \
['blessed>=1.17.9,<2.0.0',
 'coleo>=0.1.7,<0.2.0',
 'hrepr>=0.2.4,<0.3.0',
 'requests>=2.24.0,<3.0.0',
 'tqdm>=4.48.2,<5.0.0']

entry_points = \
{'console_scripts': ['paperoni = paperoni.__main__:main'],
 'paperoni.command': ['bibtex = '
                      'paperoni.commands.command_bibtex:command_bibtex',
                      'collect = '
                      'paperoni.commands.command_collect:command_collect',
                      'config = '
                      'paperoni.commands.command_config:command_config',
                      'html = paperoni.commands.command_html:command_html',
                      'researcher = '
                      'paperoni.commands.command_researcher:command_researcher',
                      'search = '
                      'paperoni.commands.command_search:command_search']}

setup_kwargs = {
    'name': 'paperoni',
    'version': '0.1.2',
    'description': 'Search for scientific papers',
    'long_description': None,
    'author': 'Olivier Breuleux',
    'author_email': 'breuleux@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
