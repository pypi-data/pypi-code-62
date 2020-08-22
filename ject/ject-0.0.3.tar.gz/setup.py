# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ject', 'ject.length', 'ject.oneself', 'ject.pipe', 'ject.pipe.predicates']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ject',
    'version': '0.0.3',
    'description': 'functional extensions',
    'long_description': '# ject\n#### functional extensions\n\n### Features\n- length: get length of function parameters\n- oneself: returns the parameter itself\n- pipe: pipe chain of functions\n\n### Usage\n#### get length of function parameters\n```python\nfrom ject import length\n\ndef fun(a, b, *args, **kwargs): return a, b, args, kwargs\n\nprint(length(fun)) # 4\n```\n\n#### pipe chain of functions\n```python\nfrom ject import pipe\n\ndef add_one(n): return n + 1\ndef times_two(n): return n * 2\n\nadd_one_then_times_two = pipe(add_one, times_two)\nprint(add_one_then_times_two(4))  # 10\n```',
    'author': 'Hoyeung Wong',
    'author_email': 'hoyeungw@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pydget/ject',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
