# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scifin',
 'scifin.classifier',
 'scifin.exceptions',
 'scifin.fouriertrf',
 'scifin.geneticalg',
 'scifin.marketdata',
 'scifin.montecarlo',
 'scifin.neuralnets',
 'scifin.statistics',
 'scifin.timeseries']

package_data = \
{'': ['*']}

install_requires = \
['IPython>=7.13.0,<8.0.0',
 'matplotlib>=3.1.3,<4.0.0',
 'numpy>=1.18.1,<2.0.0',
 'pandas<=1.0.3',
 'pandas_datareader>=0.8.1,<0.9.0',
 'pytz>=2019.3,<2020.0',
 'requests>=2.23.0,<3.0.0',
 'scikit-learn>=0.23.0,<0.24.0',
 'scipy>=1.4.1,<2.0.0',
 'statsmodels>=0.11.0,<0.12.0']

entry_points = \
{'console_scripts': ['scifin = scifin:main']}

setup_kwargs = {
    'name': 'scifin',
    'version': '0.1.0',
    'description': 'SciFin is a python package for Science and Finance.',
    'long_description': '\n<p align="center">\n  <img src="https://raw.githubusercontent.com/SciFin-Team/SciFin/master/docs/logos/logo_scifin_github.jpg" width=400 title="hover text">\n</p>\n\n\n\n# SciFin\n\nSciFin is a python package for Science and Finance.\n\n## Summary\n\nThe SciFin package is a Python package designed to gather and develop methods for scientific studies and financial services. It originates from the observation that numerous methods developed in scientific fields (such as mathematics, physics, biology and climate sciences) have direct applicability in finance and that, conversely, multiple methods developed in finance can benefit science.\n\nThe development goal of this package is to offer a toolbox that can be used both in research and business. Its purpose is not only to bring these fields together, but also to increase interoperability between them, helping science turn into business and finance to get new insights from science. Some functions are thus neutral to any scientific or economical fields, while others are more specialized to precise tasks. The motivation behind this design is to provide tools that perform advanced tasks while remaining simple (not depending on too many parameters).\n\n\n## Table of Contents\n\n- **[Development Stage](#development-stage)**<br>\n- **[Installation](#installation)**<br>\n- **[Usage](#usage)**<br>\n- **[Contributing](#contributing)**<br>\n- **[Credits](#credits)**<br>\n- **[License](#license)**<br>\n- **[Contacts](#contacts)**<br>\n\n\n## Development Stage\n\nThe current development is focused on the following topics:\n\n| Subpackage | Short Description | Development Stage |\n| :-----: | :-----: | :-----: |\n| [`classifier`](https://github.com/SciFin-Team/SciFin/tree/master/scifin/classifier) | classification techniques | ■ □ □ □ □ |\n| [`fouriertrf`](https://github.com/SciFin-Team/SciFin/tree/master/scifin/fouriertrf) | Fourier transforms | ■ □ □ □ □ |\n| [`geneticalg`](https://github.com/SciFin-Team/SciFin/tree/master/scifin/geneticalg) | genetic algorithms | ■ ■ ■ □ □ |\n| [`marketdata`](https://github.com/SciFin-Team/SciFin/tree/master/scifin/marketdata) | reading market data | ■ □ □ □ □ |\n| [`montecarlo`](https://github.com/SciFin-Team/SciFin/tree/master/scifin/montecarlo) | Monte Carlo simulations | ■ □ □ □ □ |\n| [`neuralnets`](https://github.com/SciFin-Team/SciFin/tree/master/scifin/neuralnets) | neural networks | □ □ □ □ □ |\n| [`statistics`](https://github.com/SciFin-Team/SciFin/tree/master/scifin/statistics) | basic statistics | ■ □ □ □ □ |\n| [`timeseries`](https://github.com/SciFin-Team/SciFin/tree/master/scifin/timeseries) | time series analysis | ■ ■ ■ ■ □ |\n\nThe topics already developed are time series analysis, genetic algorithms and statistics.\n\nA lot of development still needs to be done. Other topics will also later follow.\n\n\n## Installation\n\nInstalling SciFin on Linux or Mac is very easy, you can simply run this on a terminal:  \n`pip install SciFin`  \n\nYou can also access the last version of the package [on PyPI](https://pypi.org/project/scifin/).\n\nIf you encounter problems during installation or after and think you know how the problem can be improved, please share it with me.\n\nVersion 0.0.8 may lead to a small problem from pandas. If you get an error message such as:  \n`ImportError: cannot import name \'urlencode\' from \'pandas.io.common\'`  \nit is advised to install pandas version 1.0.3 using e.g. the command line:  \n`pip install pandas==1.0.3`.\n\n\n## Usage\n\nThe code is growing fast and many classes and function acquire new features. Hence, one version can be significantly different from the previous one at the moment. That\'s what makes development exciting! But that can also be confusing.\n\nA documentation of the code should help users. Once ready, this documentation will start appearing on [SciFin\'s Wiki page](https://github.com/SciFin-Team/SciFin/wiki).\n\nIf you encounter any problem while using SciFin, please do not hesitate to report it to us by [creating an issue](https://docs.github.com/en/github/managing-your-work-on-github/creating-an-issue).\n\n\n## Contributing\n\nThe package tries to follow the style guide for Python code [PEP8](https://www.python.org/dev/peps/pep-0008/). If you find any part of the code unclear or departing from this style, please let me know. As for docstrings, the format we try to follow here is given by the [numpy doc style](https://numpydoc.readthedocs.io/en/latest/format.html).\n\nIt is strongly advised to have a fair knowledge of Python to contribute, at least a strong motivation to learn, and recommanded to read the following [Python3 Tutorial](https://www.python-course.eu/python3_course.php) before joining the project.\n\nTo know more about the (evolving) rules that make the project self-consistent and eases interaction between contributors, please refer to details in the [Contributing](https://github.com/SciFin-Team/SciFin/blob/master/CONTRIBUTING.md) file.\n\n\n## Credits\n\nAll the development up to now has been done by Fabien Nugier. New contributors will join soon.\n\n\n## License\n\nSciFin is currently developed under the MIT license.\n\nPlease keep in mind that SciFin and its developers hold no responsibility for any wrong usage or losses related to the package usage.\n\nFor more details, please refer to the [license](https://github.com/SciFin-Team/SciFin/blob/master/LICENSE).\n\n\n## Contacts\n\nIf you have comments or suggestions, please reach Fabien Nugier. Thank you very much in advance for your feedback.\n\n\n\n',
    'author': 'Fabien Nugier',
    'author_email': 'fabien.nugier@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SciFin-Team/SciFin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
