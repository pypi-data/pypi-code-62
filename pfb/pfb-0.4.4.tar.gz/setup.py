# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pfb', 'pfb.commands', 'pfb.exporters', 'pfb.importers']

package_data = \
{'': ['*']}

entry_points = \
{'pfb.plugins': ['add = pfb.commands.add',
                 'from_gen3dict = pfb.importers.gen3dict',
                 'from_json = pfb.importers.json',
                 'rename = pfb.commands.rename',
                 'show = pfb.commands.show',
                 'to_gremlin = pfb.exporters.gremlin']}

setup_kwargs = {
    'name': 'pfb',
    'version': '0.4.4',
    'description': '',
    'long_description': None,
    'author': 'CTDS UChicago',
    'author_email': 'cdis@uchicago.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
