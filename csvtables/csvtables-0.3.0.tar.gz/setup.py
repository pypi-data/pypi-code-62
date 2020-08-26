# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['csvtables']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['csvtables = csvtables.csvtables:cli']}

setup_kwargs = {
    'name': 'csvtables',
    'version': '0.3.0',
    'description': 'Converts a CSV formatted input to a readable table in text',
    'long_description': '# csvtables\nConverts a CSV formatted input to a readable table in text. The table is Markdown compatible.\n\n## Usage\nImport `convert_table` to your project and call it with a CSV formatted iterable. This can be a file or a `StringIO` object. Passing `compact=True` argument will remove all the unnecessary whitespace from the output, producing a smaller size but less readable table.\n\n### Example:\nA sample data CSV file `tests/sample_data.csv` contains a list of fictional people.\n\n#### Running from command line\n`csvtables tests/sample_data.csv` will produce a table of the data\n\n#### Running as a module\n```\n# example.py\nfrom csvtables import csvtables\ncsv_file = open("tests/sample_data.csv", "r")\ntable_string = csvtables.convert_table(csv_file)\nprint(table_string) # display the table to stdout\n```',
    'author': 'Demetris Stavrou',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
