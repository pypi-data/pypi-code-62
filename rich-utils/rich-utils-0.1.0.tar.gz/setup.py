# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rich_utils']

package_data = \
{'': ['*']}

install_requires = \
['rich>=5.2.1,<6.0.0']

setup_kwargs = {
    'name': 'rich-utils',
    'version': '0.1.0',
    'description': 'Utility methods and classes for the "rich" package.',
    'long_description': None,
    'author': 'Tim Wedde',
    'author_email': 'timwedde@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
