# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['whatsauto', 'whatsauto.status', 'whatsauto.utils']

package_data = \
{'': ['*']}

install_requires = \
['uiautomator2>=2.11.0,<3.0.0']

setup_kwargs = {
    'name': 'whatsauto',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'hexatester',
    'author_email': 'revolusi147id@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
