# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nannernest']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=7.2.0,<8.0.0',
 'click-spinner>=0.1.10,<0.2.0',
 'colorama>=0.4.3,<0.5.0',
 'matplotlib>=3.3.0,<4.0.0',
 'nest2D==0.4.3',
 'numpy>=1.19.1,<2.0.0',
 'scikit-image>=0.17.2,<0.18.0',
 'scipy>=1.5.2,<2.0.0',
 'seaborn>=0.10.1,<0.11.0',
 'svgpath2mpl>=0.2.1,<0.3.0',
 'sympy>=1.6.1,<2.0.0',
 'torch>=1.6.0,<2.0.0',
 'torchvision>=0.7.0,<0.8.0',
 'typer>=0.3.1,<0.4.0']

entry_points = \
{'console_scripts': ['nannernest = nannernest.cli:app']}

setup_kwargs = {
    'name': 'nannernest',
    'version': '0.1.3',
    'description': 'Optimal peanut butter and banana sandwiches',
    'long_description': "# nannernest\n\n![Python package](https://github.com/EthanRosenthal/nannernest/workflows/Python%20package/badge.svg?branch=master)\n\nA small package for optimizing banana coverage on peanut butter and banana sandwiches.\n\n\n![assets/perfect_sandwich.jpg](assets/perfect_sandwich.jpg)\n\n\n## Installation\n\n`nannernest` is generally pip installable. Due to some C dependencies with the nesting library that I use [nest2D](https://github.com/markfink/nest2D), along with an outstanding [PR](https://github.com/markfink/nest2D/pull/2), I would recommend the following way to install everything:\n\n First, make sure you have [boost](https://www.boost.org/) and [cmake](https://cmake.org/) installed. If you are on Linux, then you may have `cmake` installed, and you can install `boost` with \n \n ```commandline\nsudo apt-get install libboost-all-dev \n```\n \n I'm on a Mac, and I installed `cmake` with conda and `boost` with brew:\n \n ```commandline\nconda install cmake\nbrew install boost\n```\n\nNext, pip install my fork of `nest2D`:\n\n```commandline\npip install git+https://github.com/EthanRosenthal/nest2D.git@download-dependencies\n```\n\nFinally, pip install `nannernest`\n\n```commandline\npip install nannernest\n```\n\n## Usage\n\nTake a top-down picture that contains your banana and at least one slice of bread. Pass the image in via command line:\n\n```commandline\n$ nannernest my_image.jpg\n```\n\n### CLI Details\n\n```commandline\n$ nannernest --help\nUsage: nannernest [OPTIONS] IMAGE_PATH\n\nArguments:\n  IMAGE_PATH  Image file which contains bread and banana  [required]\n\nOptions:\n  --num-slices INTEGER            Total number of slices to cut the banana\n                                  into. This number defines the slice\n                                  thickness.  [default: 22]\n\n  --mask-threshold FLOAT          Threshold of segmentation mask.  [default:\n                                  0.6]\n\n  --peel-scaler FLOAT             Fraction of slice that is assumed to belong\n                                  to banana insides versus the peel.\n                                  [default: 0.8]\n\n  --ellipse-ratio FLOAT           Assumed ratio of minor axis to major axis of\n                                  banana slice ellipses  [default: 0.85]\n\n  --plot-segmentation / --no-plot-segmentation\n                                  Whether or not to plot the segmentation\n                                  masks  [default: False]\n\n  --plot-slicing / --no-plot-slicing\n                                  Whether or not to plot the slicing circle\n                                  and skeleton  [default: False]\n\n  --output TEXT                   Name of file to output  [default:\n                                  perfect_sandwich.jpg]\n```\n",
    'author': 'Ethan Rosenthal',
    'author_email': 'ethan@ethanrosenthal.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/EthanRosenthal/nannernest',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
