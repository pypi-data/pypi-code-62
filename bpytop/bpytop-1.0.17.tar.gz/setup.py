# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['bpytop']
install_requires = \
['psutil>=5.7.0,<6.0.0']

entry_points = \
{'console_scripts': ['bpytop = bpytop:main']}

setup_kwargs = {
    'name': 'bpytop',
    'version': '1.0.17',
    'description': 'Resource monitor that shows usage and stats for processor, memory, disks, network and processes.',
    'long_description': None,
    'author': 'Aristocratos',
    'author_email': 'jakob@qvantnet.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
