# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['termlog', 'termlog.tests']

package_data = \
{'': ['*']}

install_requires = \
['pygments>=2.6.1,<3.0.0']

setup_kwargs = {
    'name': 'termlog',
    'version': '1.3.5',
    'description': 'A Terminal logging library',
    'long_description': "======\nReadme\n======\n\nTermlog\n=======\n\n.. image:: http://img.shields.io/badge/license-MIT-brightgreen.svg\n    :target: http://opensource.org/licenses/MIT\n\n.. image:: https://badge.fury.io/py/termlog.svg\n    :target: https://pypi.python.org/pypi/termlog\n\n.. image:: https://github.com/brianbruggeman/termlog/workflows/Latest%20Stable/badge.svg\n    :target: https://github.com/brianbruggeman/termlog/actions\n\n.. image:: https://codecov.io/gh/brianbruggeman/termlog/branch/stable/graph/badge.svg?token=y6xPnPtcdc\n    :target: https://codecov.io/gh/brianbruggeman/termlog\n\n\nTermlog: A terminal logging library for logging data both as lexed text or json\n\n\nMotivation\n==========\n\nI love f-strings and I wanted a method of displaying\nbeautiful f-strings in command-line interfaces.\nHowever, I needed a way of simultaneously creating a\ndeveloper friendly text log and producing structured\ntext that could be interpreted by a log-shipper in a\nclustered environment.\n\nTermlog will...\n\n* wrap print statements with a new method, `echo`\n* `echo` is fully compatible with print and is meant\n  to be a drop-in replacement\n* `echo` can immediately control: color, json,\n  timestamp, time-format outputs on each invocation\n* Alternatively, a `set_config` command can set the\n  library to use a specific configuration for each subsequent call to `echo`\n\n\nUsage\n=====\n\n.. code-block:: python\n\n     from termlog import blue, echo, red, rgb, set_config\n\n     key = 'abc'\n     value = 123\n\n     set_config(color=True, json=False)\n\n     echo(f'{red(key)}: {blue(value)}')\n     echo(f'{rgb(message=key, red=71, green=61, blue=139)}: {blue(value)}')\n     echo(f'{key}: {blue(value)}', color=True)\n\n\n\nInstallation\n============\n\nTo install termlog, simply run the following.\n\n.. code-block:: bash\n\n    $ pip install termlog\n\n\n.. include::./CONTRIBUTING.rst\n\n",
    'author': 'Brian Bruggeman',
    'author_email': 'Brian.M.Bruggeman@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/brianbruggeman/termlog',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
