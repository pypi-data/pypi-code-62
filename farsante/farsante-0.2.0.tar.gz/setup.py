# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['farsante']

package_data = \
{'': ['*']}

install_requires = \
['dask[dataframe]>=2.23.0,<3.0.0',
 'mimesis>=4.0.0,<5.0.0',
 'pandas>=1.0.0',
 'pyspark>=2.0.0']

setup_kwargs = {
    'name': 'farsante',
    'version': '0.2.0',
    'description': 'Fake DataFrame generators for Pandas and PySpark',
    'long_description': None,
    'author': 'MrPowers',
    'author_email': 'matthewkevinpowers@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1',
}


setup(**setup_kwargs)
