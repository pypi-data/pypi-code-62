# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nlcli']

package_data = \
{'': ['*']}

install_requires = \
['fann2==1.0.7', 'padatious']

setup_kwargs = {
    'name': 'nlcli',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'João Rafael',
    'author_email': 'joaoraf@me.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
