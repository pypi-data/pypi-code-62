# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gitbundle']

package_data = \
{'': ['*'], 'gitbundle': ['_config/*', 'branch/*', 'repository/*']}

install_requires = \
['pyfony-bundles>=0.2.0,<0.3.0', 'pygit2>=0.28.0,<0.29.0']

setup_kwargs = {
    'name': 'git-bundle',
    'version': '0.1.0b1',
    'description': 'Provides GIT focused parameters and classes',
    'long_description': '# git-bundle\n\nGit bundle for the Pyfony framework\n',
    'author': 'Jiri Koutny',
    'author_email': 'jiri.koutny@datasentics.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pyfony/git-bundle',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<3.8.0',
}


setup(**setup_kwargs)
