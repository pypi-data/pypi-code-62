# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['rapidapi']

package_data = \
{'': ['*']}

install_requires = \
['django>=3.1,<4.0',
 'mkdocs-material[docs]>=5.5.9,<6.0.0',
 'mkdocs[docs]>=1.1.2,<2.0.0']

setup_kwargs = {
    'name': 'django-rapidapi',
    'version': '0.1.0.dev0',
    'description': 'Django API extension',
    'long_description': '# Django RapidAPI (in progress)\n\nDjango Rapid API extension.\n\n*Inspired by [FastAPI](https://fastapi.tiangolo.com/) and [Django Rest Framework](https://www.django-rest-framework.org/).*\n\n![tests](https://github.com/antonrh/django-radidapi/workflows/tests/badge.svg)\n[![codecov](https://codecov.io/gh/antonrh/django-radidapi/branch/master/graph/badge.svg)](https://codecov.io/gh/antonrh/django-radidapi)\n[![Documentation Status](https://readthedocs.org/projects/django-radidapi/badge/?version=latest)](https://django-radidapi.readthedocs.io/en/latest/?badge=latest)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![version](https://img.shields.io/pypi/v/django-radidapi.svg)](https://pypi.org/project/django-radidapi/)\n[![license](https://img.shields.io/pypi/l/django-radidapi)](https://github.com/antonrh/django-radidapi/blob/master/LICENSE)\n\n---\n\nDocumentation: https://django-rapidapi.readthedocs.io/\n\n---\n\n## Installing\n\nInstall using `pip`:\n\n```bash\npip install django-radidapi\n```\n\n## TODO:\n\n* Documentation\n* OpenAPI support (Swagger, ReDoc)\n* Pydantic support\n* Async views support (with Django 3.1)\n* etc.\n',
    'author': 'Anton Ruhlov',
    'author_email': 'antonruhlov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/antonrh/django-apirouter',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
