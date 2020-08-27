# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['justnow']

package_data = \
{'': ['*']}

install_requires = \
['lark-parser>=0.9.0,<0.10.0']

setup_kwargs = {
    'name': 'justnow',
    'version': '0.1.4',
    'description': 'A systemd.timer inspired event parser in pure Python.',
    'long_description': '# justnow\n\n`justnow` is a systemd.timer inspired event parser in pure Python. The library consists of a [lark](https://github.com/lark-parser/lark) grammar definition and some code to parse and generate datetimes.\n\n## Usage\n\nBelow is a snippet of the basic usage.\n\n```python\nimport datetime\n\nfrom justnow.parser import EventParser\n\nreference_date = datetime.datetime(2020, 1, 1)\n\n# "sat *-*-* 14:00:00" => Generate all Saturdays at 14:00:00\nparser = EventParser("sat *-*-* 14:00:00", reference_date=reference_date)\n\nnext(parser)  # datetime.datetime(2020, 1, 4, 14, 0)\n\n# "sat *-02-29" => Generate all Saturdays which occur on a leap year\nparser = EventParser("sat *-02-29", reference_date=reference_date)\n\nlist(parser.get_next_n(limit=2))  # [datetime.datetime(2020, 2, 29, 0, 0), datetime.datetime(2048, 2, 29, 0, 0)]\n```\n\nThe `justnow` grammar defines a `time event` and is made of up 3 sections:\n\n### Weekday section\n\nThis section allows for a comma separated list of weekday names and weekday ranges.\n\n#### Weekday names\n\nThe following are valid tokens for the weekday section:\n\n- mon\n- tue\n- wed\n- thu\n- fri\n- Mon\n- Tue\n- Wed\n- Thu\n- Fri\n- monday\n- tuesday\n- wednesday\n- thursday\n- friday\n\n#### Weekday ranges\n\nA weekday range consists of two day names separated by two full stops.\n\nFor example  `mon..wed` will evaluate into mon, tue and wed.\n\n### Date section\n\nThe date section is made up of 3 sub sections, namely:\n\n- A year section\n- A month section\n- A day section\n\nEach of the above sub sections can be either:\n\n- One of more fixed length strings made up of integers separated by a comma. The length is 4 for years and 2 for months and days.\n- A wildcard `*`\n\n### Time section\n\nThe time section is made up of 3 sub sections, namely:\n\n- A hour section\n- A minute section\n- A second section\n\nEach of the above sub sections can be either:\n\n- One of more strings made up of 2 integers separated by a comma.\n- A wildcard `*`\n\n### Named Events\n\n`justnow` also supports a set of built in named events including:\n\n- `@minutely`\n- `@hourly`\n- `@daily`\n- `@monthly`\n- `@weekly`\n- `@yearly`\n- `@quarterly`\n- `@semiannually`\n- `@annually`',
    'author': 'Bradley Stuart Kirton',
    'author_email': 'bradleykirton@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/BradleyKirton/justnow',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
