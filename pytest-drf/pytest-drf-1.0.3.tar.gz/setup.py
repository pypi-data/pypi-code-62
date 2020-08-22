# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_drf',
 'pytest_drf.util',
 'tests',
 'tests.pytest_drf',
 'tests.testapp',
 'tests.testapp.views']

package_data = \
{'': ['*']}

modules = \
['pytest', 'LICENSE', 'CHANGELOG']
install_requires = \
['djangorestframework>3',
 'inflection>=0.3.1,<0.4.0',
 'pytest-assert-utils>=0,<1',
 'pytest-common-subject>=1.0,<2.0',
 'pytest-lambda>=1.1,<2.0',
 'pytest>=3.6']

entry_points = \
{'pytest11': ['drf = pytest_drf.plugin']}

setup_kwargs = {
    'name': 'pytest-drf',
    'version': '1.0.3',
    'description': 'A Django REST framework plugin for pytest.',
    'long_description': '# pytest-drf\n\n[![PyPI version](https://badge.fury.io/py/pytest-drf.svg)](https://badge.fury.io/py/pytest-drf)\n[![Build Status](https://travis-ci.org/theY4Kman/pytest-drf.svg?branch=master)](https://travis-ci.org/theY4Kman/pytest-drf)\n\npytest-drf is a [pytest](http://pytest.org) plugin for testing your [Django REST Framework](https://www.django-rest-framework.org/) APIs.\n\nMuch like Django REST Framework offers conventions and conveniences to ease the development of Django-powered APIs, pytest-drf offers conventions and conveniences to ease the development of DRF API tests.\n\nWhere DRF provides API Views, pytest-drf provides `APIViewTest`\n```python\n\n```\n',
    'author': 'Zach "theY4Kman" Kanzler',
    'author_email': 'they4kman@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/theY4Kman/pytest-drf',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
