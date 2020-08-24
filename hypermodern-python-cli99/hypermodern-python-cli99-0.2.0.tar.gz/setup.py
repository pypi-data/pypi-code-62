# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['hypermodern_python_cli99']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'desert>=2020.1.6,<2021.0.0',
 'marshmallow>=3.7.1,<4.0.0',
 'requests>=2.24.0,<3.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=1.7.0,<2.0.0'],
 ':python_version >= "3.8" and python_version < "4.0" and sys_platform == "linux"': ['torch>=1.6.0,<2.0.0']}

entry_points = \
{'console_scripts': ['hypermodern-python = '
                     'hypermodern_python_cli99.console:main']}

setup_kwargs = {
    'name': 'hypermodern-python-cli99',
    'version': '0.2.0',
    'description': 'The hypermodern Python project',
    'long_description': '# hypermodern-python-cli99\n\n[![Tests](https://github.com/cli99/hypermodern-python-cli99/workflows/Tests/badge.svg)](https://github.com/cli99/hypermodern-python-cli99/actions?workflow=Tests)\n[![Codecov](https://codecov.io/gh/cli99/hypermodern-python-cli99/branch/master/graph/badge.svg)](https://codecov.io/gh/cli99/hypermodern-python-cli99)\n[![PyPI](https://img.shields.io/pypi/v/hypermodern-python-cli99.svg)](https://pypi.org/project/hypermodern-python-cli99/)\n[![Read the Docs](https://readthedocs.org/projects/hypermodern-python-cli99/badge/)](https://hypermodern-python-cli99.readthedocs.io/)\n\nhttps://github.com/cjolowicz/hypermodern-python\n\nhttps://cjolowicz.github.io/posts/hypermodern-python-01-setup/\n\n> **_NOTE:_** this package does not publish to PyPI due to the package name conflict, the badge shows the original package.\n\n## Use Poetry to manage Black, Flake8, and the other tools as development dependencies\n\n```\npoetry add --dev \\\n    black \\\n    flake8 \\\n    flake8-bandit \\\n    flake8-black \\\n    flake8-bugbear \\\n    flake8-import-order \\\n    safety\n```\n\n## Use pre-commit\n\n```\npip install --user --upgrade pre-commit\n```\n\n## Use xdoctest to run documentation exmamples\n\n```\npoetry add --dev xdoctest\n```\n\n## Create documenation with Sphinx\n\n```\npoetry add --dev sphinx\n```\n',
    'author': 'Cheng Li',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cli99/hypermodern-python-cli99',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
