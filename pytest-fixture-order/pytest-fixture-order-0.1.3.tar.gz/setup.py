# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_fixture_order', 'tests']

package_data = \
{'': ['*']}

modules = \
['pytest', 'tox', 'LICENSE', 'CHANGELOG', 'README']
install_requires = \
['pytest>=3.0']

entry_points = \
{'pytest11': ['fixture_order = pytest_fixture_order.plugin']}

setup_kwargs = {
    'name': 'pytest-fixture-order',
    'version': '0.1.3',
    'description': 'pytest plugin to control fixture evaluation order',
    'long_description': '# pytest-fixture-order\nUse markers to control the order in which fixtures are evaluated.\n',
    'author': 'Zach "theY4Kman" Kanzler',
    'author_email': 'they4kman@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/theY4Kman/pytest-fixture-order',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
