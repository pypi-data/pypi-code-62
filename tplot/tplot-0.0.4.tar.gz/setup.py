# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tplot']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.3,<0.5.0', 'numpy>=1.11,<2.0', 'termcolor>=1.1.0,<2.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.0,<2.0']}

setup_kwargs = {
    'name': 'tplot',
    'version': '0.0.4',
    'description': 'Create text-based graphs',
    'long_description': '# tplot\n\nPackage for creating text-based graphs. Useful for visualizating data in the terminal.',
    'author': 'Jeroen Delcour',
    'author_email': 'jeroendelcour@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/JeroenDelcour/tplot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
