# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['panaetius']

package_data = \
{'': ['*']}

install_requires = \
['pylite>=0.1.0,<0.2.0', 'toml>=0.10.0,<0.11.0']

setup_kwargs = {
    'name': 'panaetius',
    'version': '1.1',
    'description': 'Python module to gracefully handle a .config file/environment variables for scripts, with built in masking for sensitive options. Provides a Splunk friendly formatted logger instance.',
    'long_description': 'Author\n=======\n\nDaniel Tomlinson (dtomlinson@panaetius.co.uk)\n\nRequires\n=========\n\n`>= python3.7`\n\nPython requirements\n====================\n\n- toml = "^0.10.0"\n- pylite = "^0.1.0"\n\nDocumentation\n==============\n\nRead the documentation on `read the docs`_.\n\n.. _read the docs: https://panaetius.readthedocs.io/en/latest/introduction.html\n\nInstallation\n==============\n\nYou can install ``panaetius`` the following ways:\n\nPython\n-------\n\n.. Attention:: You should install in a python virtual environment\n\nFrom pypi using pip\n~~~~~~~~~~~~~~~~~~~~\n\n.. code-block:: bash\n\n    pip install panaetius\n\nFrom local wheel\n~~~~~~~~~~~~~~~~~\n\nDownload the latest verion from the `releases`_ page.\n\n.. _releases: https://github.com/dtomlinson91/panaetius/releases\n\nInstall with pip:\n\n.. code-block:: bash\n\n    pip install -U panaetius-1.0.2-py3-none-any.whl\n\n\nFrom source\n~~~~~~~~~~~~\n\nClone the repo and install using ``setup.py``:\n\n.. code-block:: bash\n\n    python setup.py\n',
    'author': 'dtomlinson',
    'author_email': 'dtomlinson@panaetius.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dtomlinson91/panaetius',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
