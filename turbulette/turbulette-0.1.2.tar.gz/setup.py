# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['turbulette',
 'turbulette.alembic',
 'turbulette.apps',
 'turbulette.apps.auth',
 'turbulette.apps.auth.resolvers.queries',
 'turbulette.apps.base',
 'turbulette.apps.base.resolvers.mutations',
 'turbulette.apps.base.resolvers.queries',
 'turbulette.apps.base.resolvers.scalars',
 'turbulette.asgi',
 'turbulette.conf',
 'turbulette.core',
 'turbulette.core.validation',
 'turbulette.db',
 'turbulette.test',
 'turbulette.type',
 'turbulette.utils']

package_data = \
{'': ['*'],
 'turbulette.apps.auth': ['graphql/queries/*', 'graphql/types/*'],
 'turbulette.apps.base': ['graphql/mutations/*',
                          'graphql/queries/*',
                          'graphql/scalars/*']}

install_requires = \
['alembic>=1.4.2,<2.0.0',
 'ariadne>=0.11.0,<0.12.0',
 'gino[starlette]>=1.0.1,<2.0.0',
 'passlib[bcrypt]>=1.7.2,<2.0.0',
 'psycopg2-binary>=2.8.5,<3.0.0',
 'pydantic[email]>=1.6.1,<2.0.0',
 'python-jwt>=3.2.6,<4.0.0',
 'simple-settings>=0.19.1,<0.20.0']

entry_points = \
{'pytest11': ['turbulette = turbulette.test.pytest_plugin']}

setup_kwargs = {
    'name': 'turbulette',
    'version': '0.1.2',
    'description': 'A Framework to build async GraphQL APIs with Ariadne and GINO',
    'long_description': None,
    'author': 'Gazorby',
    'author_email': 'gazorby@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
