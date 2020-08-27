# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sqldiffer', 'sqldiffer.db']

package_data = \
{'': ['*']}

install_requires = \
['pymysql>=0.10.0,<0.11.0']

entry_points = \
{'console_scripts': ['sqldiffer = sqldiffer.main:main']}

setup_kwargs = {
    'name': 'sqldiffer',
    'version': '0.1.0',
    'description': 'Check the difference of MySQL schema (CREATE TABLE)',
    'long_description': '# sqldiffer\n\nCheck the difference of MySQL schema (CREATE TABLE)\n\n<!-- TOC depthFrom:2 -->\n\n- [Feature](#feature)\n- [Installation](#installation)\n- [Usage](#usage)\n- [Examples](#examples)\n  - [Check the differences](#check-the-differences)\n  - [Ignore charset](#ignore-charset)\n  - [Ignore auto_increment and charset](#ignore-auto_increment-and-charset)\n\n<!-- /TOC -->\n\n## Feature\n\n- Check the difference of MySQL schema\n  - Compare CREATE TABLE\n  - Choose whether to ignore AUTO_INCREMENT and CHARSET\n- Output HTML\n  - Save the difference for each table in HTML (Click [here](./tests/result.html) for sample)\n\n## Installation\n\n```bash\npip install sqldiffer\n```\n\n## Usage\n\n```\nsqldiffer -h\nusage: sqldiffer [-h] --server1 SERVER1 --server2 SERVER2 [-o OUTPUT_DIR] [--skip-auto-increment] [--skip-charset] [-V]\n\nCheck the difference of MySQL schema (CREATE TABLE)\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --server1 SERVER1     Comparison source. [Format] user:password@host:port/database\n  --server2 SERVER2     Comparison target. [Format] user:password@host:port/database\n  -o OUTPUT_DIR, --output-dir OUTPUT_DIR\n                        Directory to save files. Default is current directory.\n  --skip-auto-increment\n                        Whether to ignore the difference of "AUTO_INCREMENT=[0-9]+"\n  --skip-charset        Whether to ignore the difference of "CHARSET=[a-z0-9]+"\n  -V, --version         Show command version\n```\n\n## Examples\n\n### Check the differences\n\n```bash\nsqldiffer --server1 homoluctus:test@aroundtheworld:3306/aaa \\\n          --server2 homoluctus:test@anothersky:3306/aaa\n```\n\n### Ignore charset\n\n```bash\nsqldiffer --server1 homoluctus:test@aroundtheworld:3306/aaa \\\n          --server2 homoluctus:test@anothersky:3306/aaa \\\n          --skip-charset\n```\n\n### Ignore auto_increment and charset\n\n```bash\nsqldiffer --server1 homoluctus:test@aroundtheworld:3306/aaa \\\n          --server2 homoluctus:test@anothersky:3306/aaa \\\n          --skip-auto-increment \\\n          --skip-charset\n```\n',
    'author': 'homoluctus',
    'author_email': 'w.slife18sy@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/homoluctus/sqldiffer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
