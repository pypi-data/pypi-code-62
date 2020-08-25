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
    'version': '0.1.2',
    'description': 'Metric learning layers with tf.keras',
    'long_description': "# Simple metric learning via tf.keras\n\nThis package provides only a few metric learning losses below;\n- ArcFace\n- AdaCos\n- CircleLoss\n\nI have been greatly inspired by [PyTorch Metric Learning](https://github.com/KevinMusgrave/pytorch-metric-learning).\n\n## Installation\n\n``` shell\n$ pip install tf-simple-metric-learning\n```\n\n## Usage\n\nProvided layers are implemented via `tf.keras.layers.Layer` API, enables;\n\n``` python\nfrom tf_simple_metric_learning.layers import ArcFace\n\narcface = ArcFace(num_classes=NUM_CLASSES, margin=MARGIN, scale=SCALE)\n```\n\nExample notebook is in [examples](https://github.com/daigo0927/tf-simple-metric-learning/tree/develop/examples) directory. Implement CircleLossCL (Class-level label version) layer top of EfficientNet and train it for [Cars196 dataset](https://ai.stanford.edu/~jkrause/cars/car_dataset.html);\n\n``` python\nimport tensorflow as tf\nfrom tf_simple_metric_learning.layers import ArcFace, AdaCos, CircleLossCL\n\ninputs = tf.keras.layers.Input([*IMAGE_SIZE, 3], dtype=tf.uint8)\nx = tf.cast(inputs, dtype=tf.float32)\nx = tf.keras.applications.efficientnet.preprocess_input(x)\n\nnet = tf.keras.applications.EfficientNetB0(include_top=False, weights='imagenet', pooling='avg')\nembeds = net(x)\n\nlabels = tf.keras.layers.Input([], dtype=tf.int32)\nlabels_onehot = tf.one_hot(labels, depth=num_classes)\n\n# Create metric learning layer\n# metric_layer = ArcFace(num_classes=num_classes, margin=0.5, scale=64)\n# metric_layer = AdaCos(num_classes=num_classes)\nmetric_layer = CircleLossCL(num_classes=num_classes, margin=0.25, scale=256)\n\nlogits = metric_layer([embeds, labels_onehot])\n\nmodel = tf.keras.Model(inputs=[inputs, labels], outputs=logits)\nmodel.summary()\n```\n\n**Note that you should feed labels as input** into model in training because these layers require labels to forward.\n\nIn evaluation or prediction, above model requires both images and labels but labels is ignored in those metric learning layers. We only need to use dummy labels (ignored) with the target images because we can't access labels in evaluation or prediction.\n\n## References\n- https://github.com/KevinMusgrave/pytorch-metric-learning\n- https://github.com/scikit-learn-contrib/metric-learn\n",
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
