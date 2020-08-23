# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['way', 'way.fs']

package_data = \
{'': ['*']}

install_requires = \
['ject>=0.0.3,<0.0.4']

setup_kwargs = {
    'name': 'way',
    'version': '0.0.1',
    'description': 'filesystem tools',
    'long_description': "# way\n##### filesystem tools\n\n### Usage\n```python\nfrom way import get_files\n\nSRC = './'\nfiles = get_files(SRC, \n                  predicate=lambda f: not f.startswith('_'), \n                  extension='.py')\nprint(SRC, ':', files)\n```",
    'author': 'Hoyeung Wong',
    'author_email': 'hoyeungw@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pydget/way',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
