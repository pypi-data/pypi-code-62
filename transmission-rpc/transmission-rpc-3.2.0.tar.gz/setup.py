# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['transmission_rpc']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.23.0,<3.0.0',
 'typing_extensions>=3.7.4.2,<4.0.0.0',
 'yarl>=1.4.2,<2.0.0']

extras_require = \
{'docs': ['sphinx==3.2.1', 'sphinx-rtd-theme==0.5.0']}

setup_kwargs = {
    'name': 'transmission-rpc',
    'version': '3.2.0',
    'description': 'Python module that implements the Transmission bittorent client RPC protocol',
    'long_description': '# Transmission-rpc Readme\n\n[![PyPI](https://img.shields.io/pypi/v/transmission-rpc)](https://pypi.org/project/transmission-rpc/)\n[![Documentation Status](https://readthedocs.org/projects/transmission-rpc/badge/?version=stable)](https://transmission-rpc.readthedocs.io/en/stable/?badge=stable)\n[![ci](https://github.com/Trim21/transmission-rpc/workflows/ci/badge.svg)](https://github.com/Trim21/transmission-rpc/actions)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/transmission-rpc)](https://pypi.org/project/transmission-rpc/)\n[![Codecov branch](https://img.shields.io/codecov/c/github/Trim21/transmission-rpc/master)](https://codecov.io/gh/Trim21/transmission-rpc/branch/master)\n\n`transmission-rpc` is hosted by GitHub at [github.com/Trim21/transmission-rpc](https://github.com/Trim21/transmission-rpc)\n\n## Introduction\n\n`transmission-rpc` is a python module implementing the json-rpc client protocol for the BitTorrent client Transmission.\n\n## Install\n\n```bash\n$ pip install transmission-rpc>=3.0.0\n```\n\n## Documents\n\n<https://transmission-rpc.readthedocs.io/>\n\n## Developer\n\nthis project is forked from https://bitbucket.org/blueluna/transmissionrpc/overview\n\n`transmission-rpc` is licensed under the MIT license.\n\nCopyright (c) 2018-2020 Trim21\n\nCopyright (c) 2008-2014 Erik Svensson\n',
    'author': 'Trim21',
    'author_email': 'i@trim21.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Trim21/transmission-rpc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
