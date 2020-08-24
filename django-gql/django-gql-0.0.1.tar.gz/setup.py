# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['djgql', 'djgql.auth']

package_data = \
{'': ['*']}

install_requires = \
['django>=3,<4', 'python-gql<0.1']

setup_kwargs = {
    'name': 'django-gql',
    'version': '0.0.1',
    'description': '',
    'long_description': '# Django Graphql\n\n## gqlgen\n\ngqlgen is a generator tool for GraphQL.\n\n```shell script\nUsage: gqlgen [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  all             Generate all schema types\n  field-resolver  Generate field resolver.\n  type            Generate one type\n  type-resolver   Generate all schema types\n\n```\n\n\n## How to use\n\n```python\n# urls.py\nfrom django.contrib import admin\nfrom django.urls import path\n\nfrom djgql.views import GraphQLView\n\nurlpatterns = [\n    path(\'admin/\', admin.site.urls),\n    path(\'graphql/\', GraphQLView.as_view())\n]\n```\n\n```python\n# utils.py\ndef context_builder():\n    return {\'version\': 1}\n```\n\n```python\n# settings.py\nMIDDLEWARE = [\n    \'django.middleware.security.SecurityMiddleware\',\n    \'django.contrib.sessions.middleware.SessionMiddleware\',\n    \'django.middleware.common.CommonMiddleware\',\n    \'django.middleware.csrf.CsrfViewMiddleware\',\n    \'django.contrib.auth.middleware.AuthenticationMiddleware\',\n    \'django.contrib.messages.middleware.MessageMiddleware\',\n    \'django.middleware.clickjacking.XFrameOptionsMiddleware\',\n    \'djgql.auth.middleware.BasicAuthMiddleware\',\n]\nGRAPHQL_SCHEMA_FILE = os.path.join(BASE_DIR, \'starwar.gql\')\nGRAPHQL = {\n    \'SCHEMA\': \'starwar.schema.schema\',\n    \'ENABLE_PLAYGROUND\': True,\n    \'CONTEXT_BUILDER\': \'starwar.utils.context_builder\n}\n```\n\n```python\nimport typing\nfrom enum import Enum\n\nfrom django.conf import settings\nfrom gql import query, gql, type_resolver, enum_type, field_resolver\nfrom gql.build_schema import build_schema_from_file\nfrom djgql.auth import login_required\nfrom pydantic import BaseModel\n\ntype_defs = gql("""\ntype Query {\n    hello(name: String!): String!\n}\n""")\n\n\n@enum_type\nclass Episode(Enum):\n    NEWHOPE = 1\n    EMPIRE = 2\n    JEDI = 3\n\n\nclass Character(BaseModel):\n    id: typing.Text\n    name: typing.Optional[typing.Text]\n    friends: typing.Optional[typing.List[typing.Optional[\'Character\']]]\n    appears_in: typing.Optional[typing.List[typing.Optional[Episode]]]\n\n\nclass Human(Character):\n    id: typing.Text\n    name: typing.Optional[typing.Text]\n    friends: typing.Optional[typing.List[typing.Optional[Character]]]\n    appears_in: typing.Optional[typing.List[typing.Optional[Episode]]]\n    home_planet: typing.Optional[typing.Text]\n\n\nclass Droid(Character):\n    id: typing.Text\n    name: typing.Optional[typing.Text]\n    friends: typing.Optional[typing.List[typing.Optional[Character]]]\n    appears_in: typing.Optional[typing.List[typing.Optional[Episode]]]\n    primary_function: typing.Optional[typing.Text]\n\n\n@query\n@login_required\ndef hero(parent, info, episode: typing.Optional[Episode]) -> typing.Optional[Character]:\n    request = info.context[\'request\']\n    print(request.user)\n    return Human(id=\'test\')\n\n\n@field_resolver(\'Human\', \'name\')\ndef human_name(parent, info):\n    return \'Jack\'\n\n\n@type_resolver(\'Character\')\ndef resolve_character_type(obj, info, type_):\n    if isinstance(obj, Human):\n        return \'Human\'\n    if isinstance(obj, Droid):\n        return \'Droid\'\n    return None\n\n\nschema = build_schema_from_file(settings.GRAPHQL_SCHEMA_FILE)\n```',
    'author': 'syfun',
    'author_email': 'sunyu418@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/syfun/django-graphql',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
