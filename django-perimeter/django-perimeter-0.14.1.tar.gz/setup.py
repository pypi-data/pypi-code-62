# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['perimeter',
 'perimeter.management',
 'perimeter.management.commands',
 'perimeter.migrations']

package_data = \
{'': ['*'], 'perimeter': ['templates/perimeter/*']}

install_requires = \
['django>=2.2,<4.0']

setup_kwargs = {
    'name': 'django-perimeter',
    'version': '0.14.1',
    'description': 'Site-wide perimeter access control for Django projects.',
    'long_description': ".. image:: https://badge.fury.io/py/django-perimeter.svg\n    :target: https://badge.fury.io/py/django-perimeter\n\n.. image:: https://travis-ci.org/yunojuno/django-perimeter.svg?branch=master\n    :target: https://travis-ci.org/yunojuno/django-perimeter\n\n**This package now requires Python 3.7+ and Django 2.2+. For previous versions please refer to the relevant branch.**\n\nDjango Perimeter\n================\n\nPerimeter is a Django app that provides middleware that allows you to 'secure the perimeter' of your django site outside of any existing auth process that you have.\n\nWhy?\n----\n\nMost django sites have some kind of user registration and security model - a login process, decorators to secure certain URLs, user accounts - everything that comes with django.contrib.auth and associated apps (django-registration).\n\nSometimes, however, you want to simply secure the entire site to prevent prying eyes - the classic example being before a site goes live. You want to erect a secure perimeter fence around the entire thing. If you have control over your front-end web server (e.g. Apache, Nginx) then this can be used to do this using their in-built access control features. However, if you are running your app on a hosting platform you may not have admin access to these parts. Even if you do have control over your webserver, you may not want to be re-configuring it every time you want to grant someone access.\n\nThat's when you need Perimeter.\n\nPerimeter provides simple tokenised access control over your entire Django site (everything, including the admin site and login pages).\n\nHow does it work?\n-----------------\n\nOnce you have installed and enabled Perimeter, everyone requiring access will need an authorisation token (not authentication - there is nothing inherent in Perimeter to prevent people swapping / sharing tokens - that is an accepted use case).\n\nPerimeter runs as middleware that will inspect the user's ``session`` for a\ntoken. If they have a valid token, then they continue to use the site uninterrupted. If they do not have a token, or the token is invalid (expired or set to inactive), then they are redirected to the Perimeter 'Gateway', where they must enter a valid token, along with their name and email (for auditing purposes - this is stored in the database).\n\nTo create a new token you need to head to the admin site, and create a new token under the Perimeter app. If you have ``PERIMETER_ENABLED`` set to True already you won't be able to access the admin site (as Perimeter covers everything except for the perimeter 'gateway' form), and so there is a management command (``create_access_token``) that you can use to create your first token. (This is analagous to the Django setup process where it prompts you to create a superuser.)\n\nSetup\n-----\n\n1. Add 'perimeter' to your installed apps.\n2. Add 'perimeter.middleware.PerimeterAccessMiddleware' to the list of MIDDLEWARE_CLASSES\n3. Add the perimeter urls - NB must use the 'perimeter' namespace\n4. Add PERIMETER_ENABLED=True to your settings file. This setting can be used to enable or disable Perimeter in different environments.\n\n\nSettings:\n\n.. code:: python\n\n    PERIMETER_ENABLED = True\n\n    INSTALLED_APPS = (\n        ...\n        'perimeter',\n        ...\n    )\n\n    # perimeter must appear after sessions middleware as it relies on there\n    # being a valid request.session\n    MIDDLEWARE_CLASSES = [\n        ...\n        'django.contrib.sessions.middleware.SessionMiddleware',\n        'perimeter.middleware.PerimeterAccessMiddleware',\n        ...\n    ]\n\nSite urls:\n\n.. code:: python\n\n    # in site urls\n    urlpatterns = patterns(\n        '',\n        ...\n        # NB you must include the namespace, as it is referenced in the app\n        url(r'^perimeter/', include('perimeter.urls', namespace='perimeter')),\n        ...\n    )\n\nTests\n-----\n\nThe app has a suite of tests, and a ``tox.ini`` file configured to run them when using ``tox`` (recommended).\n",
    'author': 'YunoJuno',
    'author_email': 'code@yunojuno.com',
    'maintainer': 'YunoJuno',
    'maintainer_email': 'code@yunojuno.com',
    'url': 'https://github.com/yunojuno/django-perimeter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
