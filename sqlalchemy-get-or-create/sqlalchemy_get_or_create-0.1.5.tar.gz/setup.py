# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sqlalchemy_get_or_create']

package_data = \
{'': ['*']}

install_requires = \
['sqlalchemy>=1.3.0,<2.0.0']

setup_kwargs = {
    'name': 'sqlalchemy-get-or-create',
    'version': '0.1.5',
    'description': "SQLAlchemy versions of Django's get_or_create() and update_or_create()",
    'long_description': "SQLAlchemy get_or_create()\n==========================\n\nSQLAlchemy versions of Django's get_or_create() and update_or_create()\n\nInstallation\n------------\n\nTo get the latest stable release from PyPi\n\n.. code-block:: bash\n\n    pip install sqlalchemy_get_or_create\n\nUsage\n-----\n\nget_or_create(session, model, defaults=None, \\*\\*kwargs)\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\nSame as Django's `get_or_create()` but also takes the SQLAlchemy session and model\n\nupdate_or_create(session, model, defaults=None, \\*\\*kwargs)\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\nSame as Django's `update_or_create()` but also takes the SQLAlchemy session and model\n\nAcknowledgments\n===============\n\n#. Django\n#. Some code cribbed from https://skien.cc/blog/2014/01/15/sqlalchemy-and-race-conditions-implementing-get_one_or_create/\n",
    'author': 'Enrico Barzetti',
    'author_email': 'enricobarzetti@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/enricobarzetti/sqlalchemy_get_or_create',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
