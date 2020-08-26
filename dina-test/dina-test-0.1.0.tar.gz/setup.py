# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dina_test']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.1,<2.0.0']

setup_kwargs = {
    'name': 'dina-test',
    'version': '0.1.0',
    'description': '',
    'long_description': '*****************************\nThis is my first pypi package\n*****************************\n\nSteps\n=====\n\n - step 1: " install poetry and open it with vscode"\n - step 2: " "\n\n.. code-block:: c\n\n    #include <stdio.h>\n    int main()\n    {\n    printf("Hello world!")\n    return 0\n    }\n',
    'author': 'dinabandhu50',
    'author_email': 'beheradinabandhu50@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
