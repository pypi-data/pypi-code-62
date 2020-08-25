# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tplot']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.3,<0.5.0', 'numpy>=1.11,<2.0', 'termcolor>=1.1.0,<2.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.0,<2.0']}

setup_kwargs = {
    'name': 'tplot',
    'version': '0.0.5',
    'description': 'Create text-based graphs',
    'long_description': 'tplot\n=====\n\n`tplot` is a Python module for creating text-based graphs. Useful for visualizing data to the terminal or log files.\n\nFeatures\n--------\n\n- Scatter, line, horizontal/vertical bar, and image plotting\n- Supports numerical and categorical data\n- Legend\n- Automatic detection of unicode support with ascii fallback\n- Colors using ANSI escape characters (Windows supported)\n- Few dependencies\n- Lightweight\n\n\nInstallation\n------------\n\n`tplot` is available on [PyPi](https://test.pypi.org/project/tplot/):\n```bash\npip install tplot\n```\n\n\nBasic usage\n-----------\n\n```python\n   import tplot\n   fig = tplot.Figure()\n   fig.scatter([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])\n   fig.show()\n```\n\nPrints:\n\n```\n   10┤                                                                            •\n     │                                                                             \n     │                                                                    •        \n     │                                                                             \n    8┤                                                             •               \n     │                                                                             \n     │                                                     •                       \n     │                                                                             \n    6┤                                              •                              \n     │                                                                             \n     │                                      •                                      \n     │                                                                             \n    4┤                              •                                              \n     │                                                                             \n     │                       •                                                     \n     │                                                                             \n    2┤               •                                                             \n     │                                                                             \n     │        •                                                                    \n     │                                                                             \n    0┤•                                                                            \n      ┬───────┬──────┬───────┬──────┬───────┬───────┬──────┬───────┬──────┬───────┬\n      0       1      2       3      4       5       6      7       8      9      10\n```\n\n\nDocumentation\n-------------\n\nFull API reference is available on [readthedocs](https://tplot.readthedocs.io/en/latest/).',
    'author': 'Jeroen Delcour',
    'author_email': 'jeroendelcour@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/JeroenDelcour/tplot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
