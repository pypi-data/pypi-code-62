# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mkkm_mr']

package_data = \
{'': ['*']}

install_requires = \
['cvxopt>=1.2.5,<2.0.0', 'numpy>=1.19.1,<2.0.0', 'scipy>=1.5.2,<2.0.0']

setup_kwargs = {
    'name': 'mkkm-mr',
    'version': '0.2.5',
    'description': 'MKKM-MR Python Implementation',
    'long_description': '# Multiple-Kernel-k-Means-Clustering-with-Matrix-Induced-Regularization Python Implementation\nNon-official python implementation for AAAI16：Multiple Kernel k-Means Clustering with Matrix-Induced Regularization\n\n# Usage\n\n## Installation\nYou can install the package through pip with:\n\n```shell script\npip install mkkm_mr\n```\n\n## Using the module\nYou can see an example usage under [demo](./examples/demo.py)\n\n## Development\nThe project is using [poetry](https://python-poetry.org/) for reliable development.\n\nSee poetry documentation on how to install the latest version for your system:\n\n> https://python-poetry.org/docs\n\n### Setup\nAfter installing poetry, start an environment:\n\n```shell script\npoetry install\n```\n\nIf you are using PyCharm you can use [this plugin](https://plugins.jetbrains.com/plugin/14307-poetry) for setting up interpreter.\n\n### Testing\nTests are using standard `pytest` format. You can run them after the setup with:\n\n```shell script\npytest\n```\n',
    'author': 'Fma',
    'author_email': 'fmakdemir@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fmakdemir/mkkm-mr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
