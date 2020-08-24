# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['opensubtitles_dataloader']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'numpy>=1.0,<2.0', 'torch>=1.0,<2.0', 'tqdm>=4.0,<5.0']

entry_points = \
{'console_scripts': ['opensubtitles-download = '
                     'opensubtitles_dataloader.__main__:download']}

setup_kwargs = {
    'name': 'opensubtitles-dataloader',
    'version': '0.1.4',
    'description': '',
    'long_description': '# opensubtitles-dataloader\n[![PyPI version](https://badge.fury.io/py/opensubtitles-dataloader.svg)](https://badge.fury.io/py/opensubtitles-dataloader)\n\nDownload, preprocess and use sentences from the [OpenSubtitles v2018 dataset](http://opus.nlpl.eu/OpenSubtitles-v2018.php) without ever needing to load all of it into memory.\n\n## Download\nSee possible languages [here](http://opus.nlpl.eu/OpenSubtitles-v2018.php).\n````bash\nopensubtitles-download en\n````\nLoad tokenized version.\n````bash\nopensubtitles-download en --token\n````\n\n## Use in Python\n### Load\n````python\nopensubtites_dataset = OpenSubtitlesDataset(\'en\')\n````\nLoad only the first 1 million lines.\n````python\nopensubtites_dataset = OpenSubtitlesDataset(\'en\', first_n_lines=1_000_000)\n````\nGroup sentences into groups of 5.\n````python\nopensubtites_dataset = OpenSubtitlesDataset(\'en\', 5)\n````\nGroup sentences into groups ranging from 2 to 5.\n````python\nopensubtites_dataset = OpenSubtitlesDataset(\'en\', (2,5))\n````\nSplit sentences using "\\n".\n````python\nopensubtites_dataset = OpenSubtitlesDataset(\'en\', delimiter="\\n")\n````\nDo preprocessing.\n````python\nopensubtites_dataset = OpenSubtitlesDataset(\'en\', preprocess_function=my_preprocessing_function)\n````\n### Split for Training\n````python\ntrain, valid, test = opensubtites_dataset.split()\n````\nSet the fractions of the original dataset.\n````python\ntrain, valid, test = opensubtites_dataset.split([0.7, 0.15, 0.15])\n````\nUse a seed.\n````python\ntrain, valid, test = opensubtites_dataset.split(seed=42)\n````\n### Access\nindex.\n````python\ntrain, valid, text = OpenSubtitlesDataset(\'en\').splits()\ntrain[20_000]\n````\npytorch.\n````python\nfrom torch.utils.data import DataLoader\ntrain, valid, text = OpenSubtitlesDataset(\'en\').splits()\ntrain_loader = DataLoader(train, batch_size=16)\n````\n',
    'author': 'Christoph Minixhofer',
    'author_email': 'christoph.minixhofer@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
