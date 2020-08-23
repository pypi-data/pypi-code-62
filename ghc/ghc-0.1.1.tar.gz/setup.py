# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ghc']

package_data = \
{'': ['*'], 'ghc': ['templates/*']}

install_requires = \
['Jinja2>=2.11.2,<3.0.0', 'requests>=2.24.0,<3.0.0']

entry_points = \
{'console_scripts': ['ghc = ghc.ghc:main']}

setup_kwargs = {
    'name': 'ghc',
    'version': '0.1.1',
    'description': 'List up GitHub user / org repositories filtered by topics (ghc = GitHub Collector)',
    'long_description': '# ghc (GitHub Collector)\n\n![PyPI](https://img.shields.io/pypi/v/ghc)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ghc)\n![GitHub](https://img.shields.io/github/license/homoluctus/ghc)\n\nList up GitHub user / org repositories filtered by topics\n\n<!-- TOC depthFrom:2 -->\n\n- [Feature](#feature)\n- [Installtion](#installtion)\n- [Usage](#usage)\n- [Examples](#examples)\n  - [Output JSON](#output-json)\n  - [Output markdown](#output-markdown)\n- [Roadmap](#roadmap)\n\n<!-- /TOC -->\n\n## Feature\n\n- List up GitHub org repositories\n  - filtered by topics\n- Support several formats\n  - JSON\n  - Markdown\n- Output the results to stdout or file\n\n## Installtion\n\n```bash\npip install ghc\n```\n\n## Usage\n\n```\nusage: ghc [-h] [--token TOKEN] [-t [TOPICS [TOPICS ...]]] [-f {json,md}] [-o FILENAME] [-V] owner\n\nList up GitHub user / org repositories filtered by topics\n\npositional arguments:\n  owner                 Repository user or organization name to search\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --token TOKEN         Personal Access Token to access the private repository\n  -t [TOPICS [TOPICS ...]], --topics [TOPICS [TOPICS ...]]\n                        Filter repository using topics\n  -f {json,md}, --format {json,md}\n                        Format the results with json or md (markdown). Default is json\n  -o FILENAME, --output FILENAME\n                        Filename to output the results. Output stdout if not specified\n  -V, --version         Show command version\n```\n\n## Examples\n\n### Output JSON\n\n```bash\nghc homoluctus --token xxxxxxxx -f json -t python aws | jq\n```\n\n<details>\n<summary>Result</summary>\n\n```json\n{\n  "count": 2,\n  "repositories": [\n    {\n      "description": "The CLI tool to query AWS CloudWatch Logs Insights :mag:",\n      "is_archive": false,\n      "is_template": false,\n      "language": "Python",\n      "language_logo_url": "https://cdn.jsdelivr.net/npm/programming-languages-logos/src/python/python_24x24.png",\n      "name": "pyinsights",\n      "url": "https://github.com/homoluctus/pyinsights"\n    },\n    {\n      "description": "Scan the vulnerability of Docker images stored in ECR",\n      "is_archive": false,\n      "is_template": false,\n      "language": "Python",\n      "language_logo_url": "https://cdn.jsdelivr.net/npm/programming-languages-logos/src/python/python_24x24.png",\n      "name": "ecranner",\n      "url": "https://github.com/homoluctus/ecranner"\n    }\n  ]\n}\n```\n\n</details>\n\n### Output markdown\n\n\n```bash\nnghc homoluctus --token xxxxxxx -f md -t python aws\n```\n\n<details>\n<summary>Result (Raw)</summary>\n\n```markdown\n# Repositories\n\nTotal Count: 2\n\n|Name|URL|Language|Archived|Template|Description|\n|:--:|:--:|:--:|:--:|:--:|:--|\n|pyinsights|https://github.com/homoluctus/pyinsights|![Python](https://cdn.jsdelivr.net/npm/programming-languages-logos/src/python/python_24x24.png)|False|False|The CLI tool to query AWS CloudWatch Logs Insights :mag:|\n|ecranner|https://github.com/homoluctus/ecranner|![Python](https://cdn.jsdelivr.net/npm/programming-languages-logos/src/python/python_24x24.png)|False|False|Scan the vulnerability of Docker images stored in ECR|\n\n```\n\n</details>\n\n<details>\n<summary>Result</summary>\n\n# Repositories\n\nTotal Count: 2\n\n|Name|URL|Language|Archived|Template|Description|\n|:--:|:--:|:--:|:--:|:--:|:--|\n|pyinsights|https://github.com/homoluctus/pyinsights|![Python](https://cdn.jsdelivr.net/npm/programming-languages-logos/src/python/python_24x24.png)|False|False|The CLI tool to query AWS CloudWatch Logs Insights :mag:|\n|ecranner|https://github.com/homoluctus/ecranner|![Python](https://cdn.jsdelivr.net/npm/programming-languages-logos/src/python/python_24x24.png)|False|False|Scan the vulnerability of Docker images stored in ECR|\n\n</details>\n\n## Roadmap\n\n- [ ] Ignore filter\n- [ ] Output to user-defined template\n',
    'author': 'homoluctus',
    'author_email': 'w.slife18sy@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/homoluctus/gh-collector',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
