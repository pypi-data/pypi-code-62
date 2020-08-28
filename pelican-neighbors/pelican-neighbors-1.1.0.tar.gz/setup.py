# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pelican', 'pelican.plugins.neighbors']

package_data = \
{'': ['*'], 'pelican.plugins.neighbors': ['test_data/*']}

install_requires = \
['pelican>=4.5,<5.0']

extras_require = \
{'markdown': ['markdown>=3.2.2,<4.0.0']}

setup_kwargs = {
    'name': 'pelican-neighbors',
    'version': '1.1.0',
    'description': 'Neighbors is a Pelican plugin that adds Next/Previous links to articles',
    'long_description': '# Neighbor Articles: A Plugin for Pelican\n\n[![Build Status](https://img.shields.io/github/workflow/status/pelican-plugins/neighbors/build)](https://github.com/pelican-plugins/neighbors/actions) [![PyPI Version](https://img.shields.io/pypi/v/pelican-neighbors)](https://pypi.org/project/pelican-neighbors/)\n\nNeighbors is a Pelican plugin that adds Next/Previous links to articles.\n\n\n## Installation\n\nThis plugin can be installed via:\n\n    python -m pip install pelican-neighbors\n\n\n## Basic usage\n\nThis plugin adds a couple of new variables to the article\'s context:\n\n* `next_article` (newer)\n* `prev_article` (older)\n* `next_article_in_category`\n* `prev_article_in_category`\n\nHere is an example on how to add article navigation in your Jinja `article.html`\ntemplate:\n\n```html+jinja\n<ul>\n    {% if article.prev_article %}\n        <li>\n            <a href="{{ SITEURL }}/{{ article.prev_article.url}}">\n                {{ article.prev_article.title }}\n            </a>\n        </li>\n    {% endif %}\n    {% if article.next_article %}\n        <li>\n            <a href="{{ SITEURL }}/{{ article.next_article.url}}">\n                {{ article.next_article.title }}\n            </a>\n        </li>\n    {% endif %}\n</ul>\n<ul>\n    {% if article.prev_article_in_category %}\n        <li>\n            <a href="{{ SITEURL }}/{{ article.prev_article_in_category.url}}">\n                {{ article.prev_article_in_category.title }}\n            </a>\n        </li>\n    {% endif %}\n    {% if article.next_article_in_category %}\n        <li>\n            <a href="{{ SITEURL }}/{{ article.next_article_in_category.url}}">\n                {{ article.next_article_in_category.title }}\n            </a>\n        </li>\n    {% endif %}\n</ul>\n```\n\n\n## Subcategory plugin support\n\nFollowing below are instructions on how to use `Neighbors` in conjunction with\nthe [`Subcategory`\nplugin](https://github.com/getpelican/pelican-plugins/tree/master/subcategory).\n\nSince an article can belong to more than one subcategory, subcategories are\nstored in a list. If you have an article with subcategories like\n`Category/Foo/Bar`, it will belong to both subcategory `Foo`, and `Foo/Bar`.\n\nSubcategory neighbors are added to an article as `next_article_in_subcategory#`\nand `prev_article_in_subcategory#` where `#` is the level of subcategory. So\nusing the example from above, `subcategory1` will be `Foo`, and `subcategory2`\nwill be `Foo/Bar`.\n\nTherefor the usage with subcategories is:\n\n```html+jinja\n<ul>\n    {% if article.prev_article_in_subcategory1 %}\n        <li>\n            <a href="{{ SITEURL }}/{{ article.prev_article_in_subcategory1.url}}">\n                {{ article.prev_article_in_subcategory1.title }}\n            </a>\n        </li>\n    {% endif %}\n    {% if article.next_article_in_subcategory1 %}\n        <li>\n            <a href="{{ SITEURL }}/{{ article.next_article_in_subcategory1.url}}">\n                {{ article.next_article_in_subcategory1.title }}\n            </a>\n        </li>\n    {% endif %}\n</ul>\n<ul>\n    {% if article.prev_article_in_subcategory2 %}\n        <li>\n            <a href="{{ SITEURL }}/{{ article.prev_article_in_subcategory2.url}}">\n                {{ article.prev_article_in_subcategory2.title }}\n            </a>\n        </li>\n    {% endif %}\n    {% if article.next_article_in_subcategory2 %}\n        <li>\n            <a href="{{ SITEURL }}/{{ article.next_article_in_subcategory2.url}}">\n                {{ article.next_article_in_subcategory2.title }}\n            </a>\n        </li>\n    {% endif %}\n</ul>\n```\n\n\n## Contributing\n\nContributions are welcome and much appreciated. Every little bit helps. You can contribute by improving the documentation, adding missing features, and fixing bugs. You can also help out by reviewing and commenting on [existing issues][].\n\nTo start contributing to this plugin, review the [Contributing to Pelican][] documentation, beginning with the **Contributing Code** section.\n\n[existing issues]: https://github.com/pelican-plugins/neighbors/issues\n[Contributing to Pelican]: https://docs.getpelican.com/en/latest/contribute.html\n',
    'author': 'Justin Mayer',
    'author_email': 'entroP@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pelican-plugins/neighbors',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
