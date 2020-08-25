# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scenographer']

package_data = \
{'': ['*']}

install_requires = \
['commentjson>=0.8.3,<0.9.0',
 'dict-digger>=0.2.1,<0.3.0',
 'docopt>=0.6.2,<0.7.0',
 'loguru>=0.5.1,<0.6.0',
 'matplotlib>=3.1.2,<4.0.0',
 'networkx>=2.5,<3.0',
 'psycopg2-binary>=2.8.5,<3.0.0',
 'pyrsistent>=0.16.0,<0.17.0',
 'sqlalchemy-postgres-copy>=0.5.0,<0.6.0',
 'sqlalchemy>=1.3.19,<2.0.0',
 'sqlalchemy_utils>=0.36.8,<0.37.0']

entry_points = \
{'console_scripts': ['scenographer = scenographer.cli:cli']}

setup_kwargs = {
    'name': 'scenographer',
    'version': '0.1.0',
    'description': 'The cool dude who sets up the stage. Word.',
    'long_description': None,
    'author': 'Xavier Francisco',
    'author_email': 'xavier@zyper.com',
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
