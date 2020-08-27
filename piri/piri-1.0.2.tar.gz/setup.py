# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['piri']

package_data = \
{'': ['*']}

install_requires = \
['jsonschema>=3.2.0,<4.0.0',
 'pycountry==19.8.18',
 'returns>=0.14.0,<0.15.0',
 'typing_extensions==3.7.4']

setup_kwargs = {
    'name': 'piri',
    'version': '1.0.2',
    'description': 'Configurable and documentable Json transformation and mapping',
    'long_description': '# Piri\nConfigurable Data Mapping for mortals\n___\n![test](https://github.com/greenbird/piri/workflows/test/badge.svg)\n[![codecov](https://codecov.io/gh/greenbird/piri/branch/master/graph/badge.svg)](https://codecov.io/gh/greenbird/piri)\n[![Python Version](https://img.shields.io/pypi/pyversions/piri.svg)](https://pypi.org/project/piri/)\n[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)\n___\n\n**[Documentation](https://greenbird.github.io/piri/) |\n[Source Code](https://github.com/greenbird/piri) |\n[Task Tracker](https://github.com/greenbird/piri/issues)**\n\n## Goal\n\nThe goal of this library is to make JSON to JSON transformation/mapping configurable. We achieve this by using a simple but feature-rich JSON configuration which then also acts as a contract.\n\n## Features\n\n* Mapping with configuration File.\n* Transforms JSON\n* Combine multiple values to one.\n* Default values\n* If statements\n    * is, contains, not\n* casting\n    * integer, decimal, iso date\n\n## Contributing\nPlease see [contribute](../contributing)\n\n## Installation\n\nPackage is on pypi. Use pip or poetry to install\n\n```sh\npip install piri\n```\n```sh\npoetry add piri\n```\n\n## Quickstart\n```python\nimport simplejson\n\nfrom piri.process import process\n\nmy_config = {\n    \'name\': \'schema\',\n    \'array\': False,\n    \'objects\': [\n        {\n            \'name\': \'invoices\',\n            \'array\': True,\n            \'path_to_iterable\': [\'root\', \'invoices\'],\n            \'attributes\': [\n                {\n                    \'name\': \'amount\',\n                    \'mappings\': [\n                        {\n                            \'path\': [\'invoices\', \'amount\'],\n                        },\n                    ],\n                    \'casting\': {\n                        \'to\': \'decimal\',\n                        \'original_format\': \'integer_containing_decimals\',\n                    },\n                    \'default\': 0,\n                },\n                {\n                    \'name\': \'debtor\',\n                    \'mappings\': [\n                        {\n                            \'path\': [\'root\', \'customer\', \'first_name\'],\n                        },\n                        {\n                            \'path\': [\'root\', \'customer\', \'last_name\'],\n                        },\n                    ],\n                    \'separator\': \' \',\n                },\n            ],\n            \'objects\': [],\n        },\n    ],\n}\n\nexample_data = {\n    \'root\': {\n        \'customer\': {\n            \'first_name\': \'John\',\n            \'last_name\': \'Smith\',\n        },\n        \'invoices\': [\n            {\n                \'amount\': 10050,\n            },\n            {\n                \'amount\': 20050,\n            },\n            {\n                \'amount\': -15005,\n            },\n        ],\n    },\n}\n\nmapped_data = process(example_data, my_config)\n\nwith open(\'resultfile.json\', \'w\') as output_file:\n    output_file.write(simplejson.dumps(mapped_data))\n\n```\n\ncontents of resultfile.json\n```json\n{\n    "invoices": [\n        {\n            "amount": 100.5,\n            "debtor": "John Smith"\n        },\n        {\n            "amount": 200.5,\n            "debtor": "John Smith"\n        },\n        {\n            "amount": -150.05,\n            "debtor": "John Smith"\n        }\n    ]\n}\n```\n',
    'author': 'Thomas Borgen',
    'author_email': 'thomas.borgen@greenbird.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/greenbird/piri',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
