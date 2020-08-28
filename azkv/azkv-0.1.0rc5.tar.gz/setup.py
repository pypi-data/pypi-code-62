# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['azkv', 'azkv.controllers', 'azkv.core', 'azkv.ext', 'azkv.templates']

package_data = \
{'': ['*']}

install_requires = \
['azure-common>=1.1.25,<2.0.0',
 'azure-identity>=1.3.1,<1.4.0',
 'azure-keyvault-secrets>=4.2.0,<5.0.0',
 'cement>=3.0.4,<4.0.0',
 'colorlog>=4.2.1,<5.0.0',
 'jinja2>=2.11.2,<3.0.0',
 'pyyaml>=5.3.1,<6.0.0',
 'typing>=3.7.4,<4.0.0']

extras_require = \
{'code-format': ['black>=19.10b0,<20.0', 'blacken-docs>=1.7,<2.0'],
 'code-lint': ['flake8>=3.8,<4.0',
               'flake8-import-order>=0.18,<0.19',
               'flake8-bandit>=2.1,<3.0',
               'flake8-blind-except>=0.1,<0.2',
               'flake8-bugbear>=20.1,<21.0',
               'flake8-builtins>=1.5,<2.0',
               'flake8-docstrings>=1.5,<2.0',
               'flake8-logging-format>=0.6,<0.7',
               'flake8-mypy>=17.8,<18.0',
               'pep8-naming>=0.8,<0.9',
               'pygments>=2.6,<3.0'],
 'docs': ['recommonmark>=0.6.0,<0.7.0',
          'sphinx>=3.1,<4.0',
          'sphinx-rtd-theme>=0.5,<0.6',
          'sphinx-autodoc-typehints>=1.11,<2.0'],
 'test': ['pytest>=6.0,<7.0',
          'pytest-benchmark[aspect]>=3.2,<4.0',
          'pytest-cov>=2.10,<3.0',
          'pytest-instafail>=0.4,<0.5',
          'pytest-lazy-fixture>=0.6,<0.7',
          'pytest-random-order>=1.0,<2.0']}

entry_points = \
{'console_scripts': ['azkv = azkv.main:main']}

setup_kwargs = {
    'name': 'azkv',
    'version': '0.1.0rc5',
    'description': 'CLI client for the Azure Key Vault data plane',
    'long_description': '# AzKV\n\n[![Python 3.6+](https://img.shields.io/badge/Python-3.6+-blue.svg)][PythonRef] [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)][BlackRef] [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)][MITRef]\n\n[PythonRef]: https://docs.python.org/3.6/\n[BlackRef]: https://github.com/ambv/black\n[MITRef]: https://opensource.org/licenses/MIT\n\n`azkv` is a CLI client for the Azure Key Vault data plane.\n\n## Getting Started\n\n### Installing\n\nTBD\n\n### Requirements\n\n* Python >= 3.6\n\n## Built using\n\n* [Cement][CementRef] - CLI application framework\n\n[CementRef]: https://builtoncement.com/\n\n## Versioning\n\nWe use [Semantic Versioning Specification][SemVer] as a version numbering convention.\n\n[SemVer]: http://semver.org/\n\n## Release History\n\nFor the available versions, see the [tags on this repository][RepoTags]. Specific changes for each version are documented in [CHANGELOG.md][ChangelogRef].\n\nAlso, conventions for `git commit` messages are documented in [CONTRIBUTING.md][ContribRef].\n\n[RepoTags]: https://github.com/undp/azkv/tags\n[ChangelogRef]: CHANGELOG.md\n[ContribRef]: CONTRIBUTING.md\n\n## Authors\n\n* **Oleksiy Kuzmenko** - [OK-UNDP@GitHub][OK-UNDP@GitHub] - *Initial design and implementation*\n\n[OK-UNDP@GitHub]: https://github.com/OK-UNDP\n\n## Acknowledgments\n\n* Hat tip to all individuals shaping design of this project by sharing their knowledge in articles, blogs and forums.\n\n## License\n\nUnless otherwise stated, all authors (see commit logs) release their work under the [MIT License][MITRef]. See [LICENSE.md][LicenseRef] for details.\n\n[LicenseRef]: LICENSE.md\n\n## Contributing\n\nThere are plenty of ways you could contribute to this project. Feel free to:\n\n* submit bug reports and feature requests\n* outline, fix and expand documentation\n* peer-review bug reports and pull requests\n* implement new features or fix bugs\n\nSee [CONTRIBUTING.md][ContribRef] for details on code formatting, linting and testing frameworks used by this project.\n',
    'author': 'Oleksiy Kuzmenko',
    'author_email': 'oleksiy.kuzmenko@undp.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/undp/azkv',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
