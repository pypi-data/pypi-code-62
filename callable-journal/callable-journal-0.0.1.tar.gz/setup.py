# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['callable_journal']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.6.1,<2.0.0', 'pyyaml>=5.3.1,<6.0.0', 'toolz>=0.10.0,<0.11.0']

setup_kwargs = {
    'name': 'callable-journal',
    'version': '0.0.1',
    'description': 'Log message generator for callables argument and return values.',
    'long_description': '# callable-journal',
    'author': 'Nate Atkins',
    'author_email': 'atkinsnw@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nathan5280/ndl-tools',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
