# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['composetools']
setup_kwargs = {
    'name': 'composetools',
    'version': '0.4.0',
    'description': 'Utility functions for common tasks when composing functions.',
    'long_description': '# composetools\n\n**A library of utility functions** for Pythonic function composition.<br>\nMost utilities are focused on transforming and dealing with iterables.\n\n## Install\n\n```console\npip install composetools\n```\n\n## Functions\n\n* `compose`\n\n   Compose functions such that `compose(f, g)(x)` is equivalent to `g(f(x))`\n\n* `pipe`\n\n   Compose functions such that `pipe(f, g)(x)` is equivalent to `f(g(x))`\n\n### Utilities\n\n* `unique` - Yield unique items of an iterable.\n* `each` - Curried `map`.\n* `keep` - Curried `filter`.\n* `mask` - Curried `itertools.compress`.\n* `drop` - Curried `itertools.filterfalse`.\n* `sort` - Curried `sorted`.\n* `flat` - Flatten an arbitrarily nested iterable to a desired depth.\n* `also` - Call a function and return its *input*, eg. `also(print)(4)`\nwill print 4 and return 4.\n\n## Develop\n\n```console\n$ gh repo clone SeparateRecords/python-composetools\n$ poetry install\n$ poetry run python -m pytest tests.py\n```\n\n## Licence\n\nISC\n',
    'author': 'SeparateRecords',
    'author_email': 'me@rob.ac',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
