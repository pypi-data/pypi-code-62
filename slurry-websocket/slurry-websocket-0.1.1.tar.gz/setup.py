# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['slurry_websocket']

package_data = \
{'': ['*']}

install_requires = \
['slurry>=0.3.1,<0.4.0', 'trio-websocket>=0.8.0,<0.9.0', 'ujson>=3.1.0,<4.0.0']

setup_kwargs = {
    'name': 'slurry-websocket',
    'version': '0.1.1',
    'description': 'A Slurry websocket section',
    'long_description': '================\nSlurry-Websocket\n================\n\n\nCredits\n-------\n\nSmall bits of code and documentation has been copied from the `Trio-Websocket`_ library.\n\n\n\n\n\n.. _`Trio-Websocket`: https://github.com/HyperionGray/trio-websocket',
    'author': 'Anders Ellenshøj Andersen',
    'author_email': 'andersa@ellenshoej.dk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/andersea/slurry-websocket',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
