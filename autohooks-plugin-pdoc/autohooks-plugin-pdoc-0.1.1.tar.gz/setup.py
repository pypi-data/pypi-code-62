# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['autohooks', 'autohooks.plugins.pdoc']

package_data = \
{'': ['*']}

modules = \
['CHANGELOG', 'RELEASE', 'poetry']
install_requires = \
['autohooks>=1.1', 'pdoc>=0.3.2,<0.4.0']

setup_kwargs = {
    'name': 'autohooks-plugin-pdoc',
    'version': '0.1.1',
    'description': 'An autohooks plugin for python documentation via pdoc',
    'long_description': '',
    'author': 'Craig de Gouveia',
    'author_email': 'craig.degouveia@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/HughZurname/autohooks-plugin-pdoc',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
