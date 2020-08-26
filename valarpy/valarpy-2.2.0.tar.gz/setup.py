# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['valarpy']

package_data = \
{'': ['*']}

install_requires = \
['PyMySQL>=0.9,<1.0', 'pandas>=1,<2', 'peewee>=3.13,<4.0']

setup_kwargs = {
    'name': 'valarpy',
    'version': '2.2.0',
    'description': 'Python ORM to talk to Valar.',
    'long_description': '# Valarpy\n\n[![Version status](https://img.shields.io/pypi/status/valarpy)](https://pypi.org/project/valarpy/)\n[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/valarpy)](https://pypi.org/project/valarpy/)\n[![GitHub release (latest SemVer including pre-releases)](https://img.shields.io/github/v/release/dmyersturnbull/valarpy?include_prereleases&label=GitHub)](https://github.com/dmyersturnbull/valarpy/releases)\n[![Latest version on PyPi](https://badge.fury.io/py/valarpy.svg)](https://pypi.org/project/valarpy/)\n[![Documentation status](https://readthedocs.org/projects/valarpy/badge/?version=latest&style=flat-square)](https://valarpy.readthedocs.io/en/stable/)\n[![Build & test](https://github.com/dmyersturnbull/valarpy/workflows/Build%20&%20test/badge.svg)](https://github.com/dmyersturnbull/valarpy/actions)\n\nPython code to talk to [Valar](https://github.com/dmyersturnbull/valar).\nThere is more documentation available in the Valar readme.\n[See the docs](https://valarpy.readthedocs.io/en/stable/).\n\nUsage:\n\n```python\nimport valarpy\nwith valarpy.opened() as model:\n    print(list(model.Refs.select()))\n```\n\nAn example connection config file:\n\n```json\n{\n    "port": 3306,\n    "user": "kaletest",\n    "password": "kale123",\n    "database": "valartest",\n    "host": "127.0.0.1"\n}\n```\n\n[New issues](https://github.com/dmyersturnbull/valarpy/issues) and pull requests are welcome.\nPlease refer to the [contributing guide](https://github.com/dmyersturnbull/valarpy/blob/master/CONTRIBUTING.md).\nGenerated with [Tyrannosaurus](https://github.com/dmyersturnbull/tyrannosaurus).\n',
    'author': 'Douglas Myers-Turnbull',
    'author_email': None,
    'maintainer': 'Douglas Myers-Turnbull',
    'maintainer_email': None,
    'url': 'https://github.com/dmyersturnbull/valarpy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
