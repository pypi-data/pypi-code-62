# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rld', 'rld.tests', 'rld.tests.resources', 'rld.tests.resources.rollouts']

package_data = \
{'': ['*']}

install_requires = \
['captum>=0.2.0,<0.3.0',
 'click>=7.1.2,<8.0.0',
 'flask>=1.1.2,<2.0.0',
 'ray[all]>=0.8.6,<0.9.0',
 'torch>=1.6.0,<2.0.0']

entry_points = \
{'console_scripts': ['rld = rld.cli:main']}

setup_kwargs = {
    'name': 'rld',
    'version': '0.1.1',
    'description': 'A development tool for evaluation and interpretability of reinforcement learning agents.',
    'long_description': '# ![rld logo](https://imgur.com/XlDt5Hi.png)\n\n![Build and test](https://github.com/iamhatesz/rld/workflows/Build%20and%20test/badge.svg)\n\nA development tool for evaluation and interpretability of reinforcement learning agents.\n\n![rld demo gif](https://imgur.com/hodTIcj.gif)\n\n## Installation\n\n```bash\npip install rld\n```\n\n## Usage\n\nFirstly, calculate attributations for your rollout using:\n\n```bash\nrld attribute [--rllib] [--out <ROLLOUT>] config.py <INPUT_ROLLOUT>\n```\n\nThis will take `INPUT_ROLLOUT` (possibly in the Ray RLlib format, if `--rllib` is set)\nand calculate attributations for each timestep in each trajectory,\nusing the configuration stored in `config.py`.\nThe output file will be stored as `ROLLOUT`.\nSee the `Config` class for possible configuration.\n\nOnce the attributations are calculated, you can visualize them using:\n\n```bash\nrld start --viewer <VIEWER_ID> <ROLLOUT>\n```\n\nSee the [examples](./examples) for reference.\n\n## Description\n\nrld provides a set of tools to evaluate and understand behaviors of reinforcement\nlearning agents. Under the hood, rld uses [Captum](https://captum.ai/) to calculate\nattributations of observation components. rld is also integrated with\n[Ray RLlib](https://ray.io/) library and allows to load agents trained in RLlib.\n\n### Current limitations\n\nrld is currently in its early development stage, thus the functionality is very limited.\n\n#### RL algorithms\n\nrld is algorithm-agnostic, but currently it is more suitable for policy-based methods.\nThis is due to the fact that the `Model` is now expected to output logits for a given\nobservation. This, however, will change in the future, and rld will support more\nalgorithms.\n\n#### Viewers\n\nThis is the list of viewers, which ship with rld:\n* `none`\n* `cartpole`\n* `atari`\n\nYou can easily create your own viewer, for your own environment, but to make it visible\nfor rld, you have to rebuild the project. This will be improved in the future.\n\n#### Observation and action spaces\n\nThe table below presents currently supported observation and action spaces.\n\n<table>\n    <tr>\n        <td></td>\n        <td></td>\n        <td colspan="2"><strong>Action space</strong></td>\n    </tr>\n    <tr>\n        <td></td>\n        <td></td>\n        <td>Discrete</td>\n        <td>MultiDiscrete</td>\n    </tr>\n    <tr>\n        <td rowspan="3"><strong>Obs space</strong></td>\n        <td>Box</td>\n        <td>:heavy_check_mark:</td>\n        <td>:heavy_check_mark:</td>\n    </tr>\n    <tr>\n        <td>Dict</td>\n        <td>:heavy_check_mark:</td>\n        <td>:heavy_check_mark:</td>\n    </tr>\n</table>\n\n## Roadmap\n\nSee the [issues](https://github.com/iamhatesz/rld/issues) page to see the list of\nfeatures planned for the future releases. If you have your own ideas,\nyou are encouraged to post them there.\n',
    'author': 'Tomasz Wrona',
    'author_email': 'tomasz@wrona.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/iamhatesz/rld',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
