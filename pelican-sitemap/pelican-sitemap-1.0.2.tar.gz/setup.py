# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pelican', 'pelican.plugins.sitemap']

package_data = \
{'': ['*']}

install_requires = \
['pelican>=4.5,<5.0']

extras_require = \
{'markdown': ['markdown>=3.2.2,<4.0.0']}

setup_kwargs = {
    'name': 'pelican-sitemap',
    'version': '1.0.2',
    'description': 'Pelican plugin to generate sitemap in plain-text or XML format',
    'long_description': 'Sitemap\n=======\n\n[![Build Status](https://img.shields.io/github/workflow/status/pelican-plugins/sitemap/build)](https://github.com/pelican-plugins/sitemap/actions) [![PyPI Version](https://img.shields.io/pypi/v/pelican-sitemap)](https://pypi.org/project/pelican-sitemap/)\n\nThis [Pelican][] plugin generates a site map in plain-text or XML format. You can use the `SITEMAP` variable in your settings file to configure the behavior of the plugin.\n\nInstallation\n------------\n\nThis plugin can be installed via:\n\n    python -m pip install pelican-sitemap\n\nUsage\n-----\n\nThe `SITEMAP` setting must be a Python dictionary and can contain these keys:\n\n* `format`, which sets the output format of the plugin (`xml` or `txt`)\n\n* `priorities`, which is a dictionary with three keys:\n\n    - `articles`, the priority for the URLs of the articles and their translations\n\n    - `pages`, the priority for the URLs of the static pages\n\n    - `indexes`, the priority for the URLs of the index pages, such as tags, author pages, categories indexes, archives, etc.\n\n    All the values of this dictionary must be decimal numbers between `0` and `1`.\n\n* `changefreqs`, which is a dictionary with three items:\n\n    - `articles`, the update frequency of the articles\n\n    - `pages`, the update frequency of the pages\n\n    - `indexes`, the update frequency of the index pages\n\n    Valid frequency values are `always`, `hourly`, `daily`, `weekly`, `monthly`, `yearly` and `never`.\n\nYou can exclude URLs from being included in the site map via regular expressions. For example, to exclude all URLs containing `tag/` or `category/` you can use the following `SITEMAP` setting.\n\n```python\nSITEMAP = {\n    "exclude": ["tag/", "category/"]\n}\n```\n\nIf a key is missing or a value is incorrect, it will be replaced with the default value.\n\nYou can also exclude an individual URL by adding metadata to it, setting `private` to `True`.\n\nThe sitemap is saved in: `<output_path>/sitemap.<format>`\n\n> **Note:** `priorities` and `changefreqs` are information for search engines and are only used in the XML site maps. For more information, see: <https://www.sitemaps.org/protocol.html#xmlTagDefinitions>\n\n**Example**\n\nHere is an example configuration (it is also the default settings):\n\n```python\n# Where your plug-ins reside\nPLUGIN_PATHS = ["/where/you/cloned/it/pelican-plugins/",]\nPLUGINS=["sitemap",]\n\nSITEMAP = {\n    "format": "xml",\n    "priorities": {\n        "articles": 0.5,\n        "indexes": 0.5,\n        "pages": 0.5\n    },\n    "changefreqs": {\n        "articles": "monthly",\n        "indexes": "daily",\n        "pages": "monthly"\n    }\n}\n```\n\nContributing\n------------\n\nContributions are welcome and much appreciated. Every little bit helps. You can contribute by improving the documentation, adding missing features, and fixing bugs. You can also help out by reviewing and commenting on [existing issues][].\n\nTo start contributing to this plugin, review the [Contributing to Pelican][] documentation, beginning with the **Contributing Code** section.\n\n[Pelican]: https://github.com/getpelican/pelican\n[existing issues]: https://github.com/pelican-plugins/sitemap/issues\n[Contributing to Pelican]: https://docs.getpelican.com/en/latest/contribute.html\n',
    'author': 'Pelican Dev Team',
    'author_email': 'authors@getpelican.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pelican-plugins/sitemap',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
