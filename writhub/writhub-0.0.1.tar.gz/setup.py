# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['writhub', 'writhub.collaters']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2==2.11',
 'PyYaml>=5.1,<6.0',
 'click>=7.1.2,<8.0.0',
 'colorama>=0.4.3,<0.5.0',
 'cssselect>=1.1.0,<2.0.0',
 'lxml>=4.5.2,<5.0.0',
 'pypandoc>=1.5,<2.0',
 'rich==5.0.0']

entry_points = \
{'console_scripts': ['writhub = writhub.console.cli:main']}

setup_kwargs = {
    'name': 'writhub',
    'version': '0.0.1',
    'description': "A static post generator, for when you don't feel like generating an entire site",
    'long_description': None,
    'author': 'Dan Nguyen',
    'author_email': 'dansonguyen@gmail.com',
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
