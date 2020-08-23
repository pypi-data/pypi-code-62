# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_codegen']

package_data = \
{'': ['*'], 'pytest_codegen': ['templates/*']}

install_requires = \
['redbaron>=0.9.2,<0.10.0', 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['ptc = pytest_codegen.__main__:entry',
                     'pytest-codegen = pytest_codegen.__main__:entry']}

setup_kwargs = {
    'name': 'pytest-codegen',
    'version': '0.0.2',
    'description': 'Automatically create pytest test signatures',
    'long_description': '# pytest-codegen\nPytest-codgen will statically analyze your code to create pytest function stubs.\n\n\n\n## Goal\nFirst working version\n\n### Future Goals\n- Create templates for tests\n- More customization\n\n\n## Disclaimer\nThis tool is currently in pre-alpha/experimental phase. Usable version will be ^0.1.x\n\n\n## Installation\n\n```\npip install pytest-codegen\n```\n\n## Usage\n\nCheck the supported commands with\n```\npytest-codegen --help\n```\nor if you are lazy like me\n```\nptc --help\n```\n\n## Suggestions & Contribution\n\nEvery suggestion and contribution is welcome\n\n## Ressources\n- [pytest-codegen on pypi](https://pypi.org/project/pytest-codegen/)\n- [redbaron on pypi](https://pypi.org/project/redbaron/)\n\n## License\nThis project is licensed under the terms of the MIT license.',
    'author': 'Jeremy Schiemann',
    'author_email': 'jeremy.schiemann@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jeremyschiemann/pytest-codegen',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
