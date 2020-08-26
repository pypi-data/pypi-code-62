# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['luxafaret']
install_requires = \
['hidapi>=0.7.99.post21,<0.8.0', 'webcolors>=1.10,<2.0']

entry_points = \
{'console_scripts': ['luxafaret = luxafaret:main']}

setup_kwargs = {
    'name': 'luxafaret',
    'version': '1.2.0',
    'description': '🐍🐑🖍🎨🌈 Luxafåret - colourize your Luxafor flag from Python',
    'long_description': None,
    'author': 'Simon Lundström',
    'author_email': 'github-commits@soy.se',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
}


setup(**setup_kwargs)
