# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_cgi', 'django_cgi.management.commands']

package_data = \
{'': ['*']}

install_requires = \
['django>=3.1,<4.0']

setup_kwargs = {
    'name': 'django-cgi',
    'version': '0.1.1',
    'description': 'Run Django with CGI',
    'long_description': 'django-cgi\n==========\n\nRun Django with CGI\n\nInstallation\n------------\n\nTo get the latest stable release from PyPi\n\n.. code-block:: bash\n\n    pip install django-cgi\n\nInstall the app\n\n.. code-block:: python\n\n    INSTALLED_APPS = (\n        ...,\n        \'django_cgi\',\n    )\n\nUsage\n-----\n\ngenerate_cgi_handler command\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n.. code-block:: bash\n\n    python manage.py generate_cgi_handler\n\nThis will create a file called cgi_handler.py next to manage.py.\n\nServer config\n-------------\n\nPoint your server to serve the cgi_handler.py file.  This is an example config for Apache:\n\n.. code-block::\n\n    LoadModule cgid_module lib/httpd/modules/mod_cgid.so\n    ScriptAlias /path "/repo/cgi_handler.py"\n    <Directory "/repo">\n        AllowOverride None\n        Options None\n        Require all granted\n    </Directory>\n',
    'author': 'Enrico Barzetti',
    'author_email': 'enricobarzetti@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/enricobarzetti/django-cgi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
