# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tutorial_server', 'tutorial_server.static', 'tutorial_server.views']

package_data = \
{'': ['*']}

install_requires = \
['decorator>=4.4.2,<5.0.0',
 'filetype>=1.0.7,<2.0.0',
 'pyramid>=1.10.4,<2.0.0',
 'requests>=2.24.0,<3.0.0',
 'waitress>=1.4.4,<2.0.0']

entry_points = \
{'paste.app_factory': ['main = tutorial_server:main']}

setup_kwargs = {
    'name': 'tutorial-server',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Mark Hall',
    'author_email': 'mark.hall@open.ac.uk',
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
