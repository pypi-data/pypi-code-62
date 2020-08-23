# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_dev']

package_data = \
{'': ['*']}

install_requires = \
['tomlkit>=0.7.0,<0.8.0', 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['poetry_dev = poetry_dev:app']}

setup_kwargs = {
    'name': 'poetry-dev',
    'version': '0.1.1',
    'description': 'A collection of scripts replace local packages with versions and vice versa',
    'long_description': '# poetry-dev\n\nWhen developing multiple Python packages concurrently with Poetry manageed environments you\ncan install the local package as path requirements. Ie when you develop `bar`\nwhich have `foo` as dependency, which you also want to edit, you can\ndo `poetry add ../foo` from `bar` package. But when you want to publish\n`bar`, you have to change the path requirement back to a version requirement.\n\nAfter publishing `bar` you have to switch back to `foo` as a path requirement\nin order to continue develop both concurrently.\n\nThis package will help you to improve that task. With one command all version\nrequirements will be changed to path requirements (when the package is\ncheckout in a sibling directory with the same as the package name).\n\n`poetry_dev path`\n\nThis results in a changed `pyproject.toml` file. `poetry update` is called\nto make sure the package on the path is installed as editable package.\n\nBefore publishing, the path requirements can be switched back to version\nrequirements with the following command.\n\n`poetry_dev version`\n\nThe version of the dependency on the local path will be\nused as minimal caret version in the changed `pyproject.toml` and\n`poetry update` is called to make sure the corresponding version\nfrom the repository will be installed.',
    'author': 'Marc Rijken',
    'author_email': 'marc@rijken.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mrijken/poetry-dev',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
