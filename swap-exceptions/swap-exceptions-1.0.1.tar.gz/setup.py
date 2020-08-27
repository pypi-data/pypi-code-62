# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['swap_exceptions']

package_data = \
{'': ['*']}

install_requires = \
['six>=1.15.0,<2.0.0']

extras_require = \
{':python_version >= "2.7" and python_version < "3.0"': ['contextlib2>=0.6.0,<0.7.0',
                                                         'typing>=3.7.4,<4.0.0']}

setup_kwargs = {
    'name': 'swap-exceptions',
    'version': '1.0.1',
    'description': 'Python utility decorator and context manager for swapping exceptions',
    'long_description': '# swap-exceptions\n\n[![PyPI](https://img.shields.io/pypi/v/swap-exceptions)](https://pypi.org/project/swap-exceptions/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/swap-exceptions)](https://pypi.org/project/swap-exceptions/)\n[![PyPI License](https://img.shields.io/pypi/l/swap-exceptions)](https://pypi.org/project/swap-exceptions/)\n[![Code Style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black/)\n\nPython utility decorator and context manager for swapping exceptions.\n\n### Basic Usage\n\nAs a decorator:\n```python\nfrom swap_exceptions import swap_exceptions\n\n@swap_exceptions({KeyError: ValueError("Incorrect value")})\ndef get_value(key: str):\n    d = {\'a\': 1, \'b\': 2}\n    return d[key]\n\nget_value(\'c\')  # ValueError: Incorrect value\n```\n\nOr as a context manager:\n```python\nfrom swap_exceptions import swap_exceptions\n\ndef get_value(key: str):\n    d = {\'a\': 1, \'b\': 2}\n    with swap_exceptions({KeyError: ValueError("Incorrect value")}):\n        return d[key]\n\nget_value(\'c\')  # ValueError: Incorrect value\n```\n\n### Advanced Usage\n\nMapping key can also be a tuple:\n```python\nfrom swap_exceptions import swap_exceptions\n\n@swap_exceptions({(KeyError, TypeError): ValueError("Incorrect value")})\ndef get_value(key: str):\n    d = {\'a\': 1, \'b\': 2, \'c\': \'not a number\'}\n    return d[key] + 10\n\nget_value(\'c\')  # ValueError: Incorrect value\n```\n\nMapping value can also be a factory that generates the exception:\n```python\nfrom swap_exceptions import swap_exceptions\n\n@swap_exceptions({KeyError: lambda e: ValueError(f"Incorrect value {e.args[0]}")})\ndef get_value(key: str):\n    d = {\'a\': 1, \'b\': 2}\n    return d[key]\n\nget_value(\'c\')  # ValueError: Incorrect value c\n```\n',
    'author': 'Tom Gringauz',
    'author_email': 'tomgrin10@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tomgrin10/swap-exceptions',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
}


setup(**setup_kwargs)
