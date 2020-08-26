# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['click_date_type']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0']

setup_kwargs = {
    'name': 'click-date-type',
    'version': '0.1.0',
    'description': 'Date type parameter for click',
    'long_description': 'click-date-type\n===============\n\nDate type parameter for click\n\nInstallation\n------------\n\nTo get the latest stable release from PyPi\n\n.. code-block:: bash\n\n    pip install click-date-type\n\nUsage\n-----\n\n.. code-block:: python\n\n    from click_date_type import Date\n\n    @click.command()\n    @click.option("--start_date", type=Date())\n    def cli(start_date):\n        click.echo(start_date.strftime("%Y-%m-%d"))\n',
    'author': 'Enrico Barzetti',
    'author_email': 'enricobarzetti@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/enricobarzetti/click-date-type',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
