# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['parchmint']

package_data = \
{'': ['*']}

install_requires = \
['networkx>=2.5,<3.0']

setup_kwargs = {
    'name': 'parchmint',
    'version': '0.1.0',
    'description': 'ParchMint object library for Python',
    'long_description': None,
    'author': 'Radhakrishna Sanka',
    'author_email': 'rkrishnasanka@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
