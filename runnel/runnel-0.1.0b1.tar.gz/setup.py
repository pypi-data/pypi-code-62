# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['runnel', 'runnel.middleware']

package_data = \
{'': ['*'], 'runnel': ['lua/*']}

install_requires = \
['aiostream>=0.4.1,<0.5.0',
 'anyio>=2.0.0-beta.2,<3.0.0',
 'aredis>=1.1.8,<2.0.0',
 'colorama>=0.4.3,<0.5.0',
 'croniter>=0.3.34,<0.4.0',
 'hiredis>=1.0.1,<2.0.0',
 'pydantic>=1.5.1,<2.0.0',
 'pytz>=2020.1,<2021.0',
 'structlog>=20.1.0,<21.0.0',
 'typer>=0.3.0,<0.4.0']

extras_require = \
{'fast': ['uvloop>=0.14.0,<0.15.0',
          'xxhash>=1.4.4,<2.0.0',
          'orjson>=3.2.1,<4.0.0',
          'lz4>=3.1.0,<4.0.0']}

entry_points = \
{'console_scripts': ['runnel = runnel.cli:cli']}

setup_kwargs = {
    'name': 'runnel',
    'version': '0.1.0b1',
    'description': 'Distributed event processing for Python based on Redis Streams',
    'long_description': '## Runnel\n\nDistributed event processing for Python based on Redis Streams.\n\nhttps://runnel.dev\n\nRunnel allows you to easily create scalable stream processors, which operate on\npartitions of event streams in Redis. Runnel takes care of assigning partitions\nto workers and acknowledging events automatically, so you can focus on your\napplication logic.\n\nWhereas traditional job queues do not provide ordering guarantees, Runnel is\ndesigned to process partitions of your event stream strictly in the order\nevents are created.\n\n### Installation\n\n```bash\npip install runnel\n```\n\n### Basic Usage\n\n```python\nfrom datetime import datetime\n\nfrom runnel import App, Record\n\napp = App(name="myapp", redis_url="redis://127.0.0.1")\n\n\n# Specify event types using the Record class.\nclass Order(Record):\n    order_id: int\n    created_at: datetime\n    amount: float\n\n\norders = app.stream("orders", record=Order, partition_by="order_id")\n\n\n# Every 4 seconds, send an example record to the stream.\n@app.timer(interval=4)\nasync def sender():\n    await orders.send(Order(order_id=1, created_at=datetime.utcnow(), amount=9.99))\n\n\n# Iterate over a continuous stream of events in your processors.\n@app.processor(orders)\nasync def printer(events):\n    async for order in events.records():\n        print(f"processed {order.amount}")\n```\n\nMeanwhile, run the worker (assuming code in `example.py` and `PYTHONPATH` is set):\n```bash\n$ runnel worker example:app\n```\n\n### Features\n\nDesigned to support a similar paradigm to Kafka Streams, but on top of Redis.\n\n* At least once processing semantics\n* Automatic partitioning of events by key\n* Each partition maintains strict ordering\n* Dynamic rebalance algorithm distributes partitions among workers on-the-fly\n* Support for nested Record types with custom serialisation and compression\n* Background tasks, including timers and cron-style scheduling\n* User-defined middleware for exception handling, e.g. dead-letter-queueing\n* A builtin batching mechanism to efficiently process events in bulk\n* A `runnel[fast]` bundle for C or Rust extension dependencies ([uvloop](https://github.com/MagicStack/uvloop), [xxhash](https://github.com/Cyan4973/xxHash), [orjson](https://github.com/ijl/orjson), [lz4](https://github.com/python-lz4/python-lz4))\n\n### Documentation\n\nFull documenation is available at https://runnel.dev.\n\n* [Guide](https://runnel.dev/guide.html)\n* [Motivation](https://runnel.dev/motivation.html)\n* [Architecture](https://runnel.dev/architecture.html)\n* [API Reference](https://runnel.dev/reference.html)\n\n### Blog posts\n\nEssays about this project or the technology it\'s using:\n\n* [Redis streams vs. Kafka](https://mattwestcott.co.uk/blog/redis-streams-vs-kafka)\n* [Structured concurrency in Python with AnyIO](https://mattwestcott.co.uk/blog/structured-concurrency-in-python-with-anyio)\n\n### Local development\n\nTo run the test suite locally, clone the repo and install the optional deps\n(e.g. via `poetry install -E fast`). Make sure Redis is running on localhost at\nport 6379, then run `pytest`.\n\n### See also\n\nFor a traditional task queue that doesn\'t provide ordering guarantees, see our\nsister project [Fennel](https://github.com/mjwestcott/fennel).\n',
    'author': 'Matt Westcott',
    'author_email': 'm.westcott@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
