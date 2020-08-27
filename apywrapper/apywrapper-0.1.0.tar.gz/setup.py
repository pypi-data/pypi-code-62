# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['apywrapper']

package_data = \
{'': ['*']}

install_requires = \
['cleo>=0.8.1,<0.9.0', 'dacite>=1.5.1,<2.0.0', 'httpx>=0.14.1,<0.15.0']

entry_points = \
{'console_scripts': ['greet = bin:main']}

setup_kwargs = {
    'name': 'apywrapper',
    'version': '0.1.0',
    'description': 'make wrapper for RESTful API',
    'long_description': None,
    'author': 'sh1ma',
    'author_email': 'in9lude@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
