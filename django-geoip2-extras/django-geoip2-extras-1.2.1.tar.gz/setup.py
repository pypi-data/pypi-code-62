# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['geoip2_extras']

package_data = \
{'': ['*']}

install_requires = \
['django>=2.2,<4.0', 'geoip2>=3.0.0,<4.0.0', 'python-env-utils']

setup_kwargs = {
    'name': 'django-geoip2-extras',
    'version': '1.2.1',
    'description': 'Additional functionality using the GeoIP2 database.',
    'long_description': ".. image:: https://badge.fury.io/py/django-geoip2-extras.svg\n    :target: https://badge.fury.io/py/django-geoip2-extras\n\n.. image:: https://travis-ci.org/yunojuno/django-geoip2-extras.svg\n    :target: https://travis-ci.org/yunojuno/django-geoip2-extras\n\n**The master branch of this project is now Python 3.7+ and Django 2.2+ only. Legacy Python and Django versions are tagged.**\n\nDjango GeoIP2 Extras\n--------------------\n\nUseful extras based on the ``django.contrib.gis.geoip2`` module, using\nthe `MaxMind GeoIP2 Lite <http://dev.maxmind.com/geoip/geoip2/geolite2/>`_ database.\n\nThe first feature in this package is a Django middleware class that can\nbe used to add city, country level information to inbound requests.\n\nRequirements\n============\n\nThis package wraps the existing Django functionality, and as a result\nrelies on the same underlying requirements:\n\n    *In order to perform IP-based geolocation, the GeoIP2 object requires the geoip2 Python library and the GeoIP Country and/or City datasets in binary format (the CSV files will not work!). Grab the GeoLite2-Country.mmdb.gz and GeoLite2-City.mmdb.gz files and unzip them in a directory corresponding to the GEOIP_PATH setting.*\n\nIn addition, the middleware follows the 'new' middleware pattern, and therefore\ndoes **not** support Django 1.9 or below. This is a 1.10 and above package.\n\nInstallation\n============\n\nThis package can be installed from PyPI as ``django-geoip2-extras``:\n\n.. code:: shell\n\n    $ pip install django-geoip2-extras\n\nIf you want to add the country-level information to incoming requests, add the\nmiddleware to your project settings. NB The ``GeoIP2Middleware`` relies on the ``SessionMiddleware``, and must come after it:\n\n.. code:: python\n\n    MIDDLEWARE = (\n        ...,\n        'django.contrib.sessions.middleware.SessionMiddleware',\n        'geoip2_extras.middleware.GeoIP2Middleware',\n        ...\n    )\n\nThe middleware will not be active unless you add a setting for\nthe default ``GEOIP_PATH`` - this is the default Django GeoIP2 behaviour:\n\n.. code:: python\n\n    # settings.py\n    GEOIP_PATH = os.path.dirname(__file__)\n\nNB Loading this package does *not* install the `MaxMind database <http://dev.maxmind.com/geoip/geoip2/geolite2/>`_.\nThat is your responsibility. The Country database is 2.7MB, and could be added to most project comfortably, but it is updated regularly, and keeping that up-to-date is out of scope for this project. The City database is 27MB, and is probably not suitable for adding to source control. There are various solutions out on the web for pulling in the City database as part of a CD process.\n\nUsage\n=====\n\nOnce the middleware is added, you will be able to access City and / or Country level\ninformation on the request object:\n\n.. code:: python\n\n    >>> request.geo_data.ip_address\n    '1.2.3.4'\n    >>> request.geo_data.city\n    'Beverley Hills'\n    >>> request.geo_data.postal_code\n    '90210'\n    >>> request.geo_data.region\n    'California'\n    >>> request.geo_data.country_code\n    'US'\n    >>> request.geo_data.country_name\n    'United States'\n    >>> request.geo_data.latitude\n    '34.0736'\n    >>> request.geo_data.longitude\n    '118.4004'\n\nMissing / incomplete data will be None.\n\nIf the IP address cannot be found (e.g. '127.0.0.1'), then a default 'unknown'\ncountry is used, with a code of 'XX':\n\n.. code:: python\n\n    >>> geo.ip_address\n    '127.0.0.1'\n    >>> geo.country_code\n    'XX'\n    >>> geo.country_name\n    'unknown'\n    >>> geo.is_unknown\n    True\n\nThis prevents the middleware from re-requesting the address on each request - it effectively marks the IP as a bad address.\n\nTests\n=====\n\nThe project tests are run through ``tox``.\n",
    'author': 'YunoJuno',
    'author_email': 'code@yunojuno.com',
    'maintainer': 'YunoJuno',
    'maintainer_email': 'code@yunojuno.com',
    'url': 'https://github.com/yunojuno/django-geoip2-extras',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
