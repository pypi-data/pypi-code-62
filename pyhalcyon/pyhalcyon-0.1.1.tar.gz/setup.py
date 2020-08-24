# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['halcyon',
 'halcyon.infer',
 'halcyon.ml',
 'halcyon.ml.net',
 'halcyon.ml.net.decoder',
 'halcyon.models']

package_data = \
{'': ['*']}

install_requires = \
['biopython==1.75',
 'click-help-colors==0.8',
 'click==7.1.2',
 'h5py==2.10.0',
 'logzero==1.5.0',
 'more-itertools==8.4.0',
 'numpy<1.17',
 'requests==2.24.0',
 'tensorflow<1.15.0',
 'ujson==1.35']

entry_points = \
{'console_scripts': ['halcyon = halcyon.console:main']}

setup_kwargs = {
    'name': 'pyhalcyon',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Hiroki Konishi',
    'author_email': 'relastle@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '==3.7.4',
}


setup(**setup_kwargs)
