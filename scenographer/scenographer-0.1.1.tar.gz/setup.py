# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scenographer']

package_data = \
{'': ['*']}

install_requires = \
['commentjson>=0.8.3,<0.9.0',
 'dict-digger>=0.2.1,<0.3.0',
 'docopt>=0.6.2,<0.7.0',
 'loguru>=0.5.1,<0.6.0',
 'matplotlib>=3.1.2,<4.0.0',
 'networkx>=2.5,<3.0',
 'psycopg2-binary>=2.8.5,<3.0.0',
 'pyrsistent>=0.16.0,<0.17.0',
 'sqlalchemy-postgres-copy>=0.5.0,<0.6.0',
 'sqlalchemy>=1.3.19,<2.0.0',
 'sqlalchemy_utils>=0.36.8,<0.37.0']

entry_points = \
{'console_scripts': ['scenographer = scenographer.cli:cli']}

setup_kwargs = {
    'name': 'scenographer',
    'version': '0.1.1',
    'description': 'The cool dude who sets up the stage. Word.',
    'long_description': '# scenographer\n\n[![PyPI pyversions](https://img.shields.io/pypi/pyversions/scenographer.svg?style=flat-square)](https://pypi.python.org/pypi/scenographer/)\n[![GitHub license](https://img.shields.io/github/license/zyperco/scenographer.svg?style=flat-square)](https://github.com/zyperco/scenographer/blob/master/LICENSE)\n[![PyPI version shields.io](https://img.shields.io/pypi/v/scenographer.svg?style=flat-square)](https://pypi.python.org/pypi/scenographer/)\n\n[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg?style=flat-square)](https://GitHub.com/zyperco/scenographer/graphs/commit-activity)\n[![zyperco](https://circleci.com/gh/zyperco/scenographer.svg?style=svg)](https://app.circleci.com/pipelines/github/zyperco/scenographer)\n\n**scenographer** is a Python script that can create a subset of a postgres database, without losing referential integrity.\n\nThe goal is to be able to spawn data-correct databases to easily create new environments that can be used for testing and / or demo\'ing.\n\nRelevant links:\n  - [Documentation](https://zyperco.github.io/scenographer/)\n\n## Installation\n\nUse [pip](https://pip.pypa.io/en/stable/) to install `scenographer`.\n\n```bash\npip install scenographer\n```\n\n## Usage\n\nScenographer requires a configuration file. An empty one, to serve as a starting point, is available by running `scenographer empty-config`.\n\nAfter adjusting the configuration file, it\'s easy to start the sampling run:\n\n```bash\nscenographer bin/scenographer sample config.json\n```\n\nor if the schema doesn\'t need to be recreated in the target database:\n\n```bash\nscenographer bin/scenographer sample config.json --skip-schema\n```\n\n## Configuration\n\n### SOURCE_DATABASE_URL\n\nThe connection string for the source database. Only Postgres is supported.\n\n### TARGET_DATABASE_URL\n\nThe connection string for the target database. Only Postgres is supported.\n\n### IGNORE_RELATIONS\n\nScenographer works by traversing a DAG graph created from the foreign key constraints of the database.\nHowever, it\'s not always the case that the database forms a DAG. To handle those cases, some foreign keys can be ignored by adding exceptions in this form:\n\n```python\nIGNORE_RELATIONS = [\n  {"pk": "product.id", "fk": "client.favorite_product_id"}\n]\n```\n\n### EXTEND_RELATIONS\n\nIn other ocasions, the actual foreign key constraint is not present in the database, although it exists in the business-side of things (like Rails does it).\nAdditional relations can be added to handle those cases. The relations take the same format of `IGNORE_RELATIONS `.\n\n### IGNORE_TABLES\n\nSome tables are _extra_. They may not matter, they may require a special solution or they are part of different components. Either way, you can ignore them.\n\n### QUERY_MODIFIERS\n\nFor some cases, it\'s useful to tap into the actual queries being made. For that, you can add an entry here. Here\'s an example:\n\n```python\nQUERY_MODIFIERS={\n    "_default": {"conditions": [], "limit": 300},\n    "users": {"conditions": ["email ilike \'%@example.com\'"]},\n}\n```\n\nEach entry is a table, with the exception of `_default` which is applied to all queries. Its values can have a `conditions` and/or `limit` key. For conditions you can write plain `sql`.\n\n\n### OUTPUT_DIRECTORY\n\nAt some point, the data is converted into CSV files to be imported into postgres. This is the directory for said CSV files. If you don\'t care about it, feel free to ignore. If it\'s not declared, it will create and use a temporary dictory instead.\n\n\n## Contributing\n\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.\n\nPlease make sure to update tests as appropriate.\n\n## License\n[MIT](https://choosealicense.com/licenses/mit/)\n',
    'author': 'Xavier Francisco',
    'author_email': 'xavier@zyper.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://zyperco.github.io/scenographer/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
