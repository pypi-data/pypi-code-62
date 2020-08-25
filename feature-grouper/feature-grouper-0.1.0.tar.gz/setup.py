# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['feature_grouper']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.1,<2.0.0', 'scikit-learn>=0.23.2,<0.24.0', 'scipy>=1.5.2,<2.0.0']

setup_kwargs = {
    'name': 'feature-grouper',
    'version': '0.1.0',
    'description': 'Simple dimensionality reduction through hierarchical clustering of correlated features.',
    'long_description': None,
    'author': 'Alex Kyllo',
    'author_email': 'alex.kyllo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
