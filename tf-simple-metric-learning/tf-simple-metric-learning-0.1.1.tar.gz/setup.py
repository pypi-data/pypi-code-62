# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tf_simple_metric_learning']

package_data = \
{'': ['*']}

install_requires = \
['tensorflow-probability>=0.11.0,<0.12.0', 'tensorflow>=2.3.0,<3.0.0']

setup_kwargs = {
    'name': 'tf-simple-metric-learning',
    'version': '0.1.1',
    'description': 'Metric learning layers with tf.keras',
    'long_description': '# keras-simple-metric-learning\nSImple metric learning methods via tf.keras\n',
    'author': 'Daigo Hirooka',
    'author_email': 'daigo.hirooka@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/daigo0927/tf-simple-metric-learning',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
