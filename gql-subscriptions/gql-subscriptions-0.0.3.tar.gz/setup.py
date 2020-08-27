# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gql_subscriptions', 'gql_subscriptions.pubsubs']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.8"': ['typing_extensions>=3.7.4,<4.0.0'],
 'redis': ['aioredis>=1.3']}

setup_kwargs = {
    'name': 'gql-subscriptions',
    'version': '0.0.3',
    'description': 'A Python3.7+ port of Apollo Graphql Subscriptions.',
    'long_description': '# gql-subscriptions\n\nA Python3.7+ port of [Apollo Graphql Subscriptions](https://github.com/apollographql/graphql-subscriptions).\n\nThis package contains a basic asyncio pubsub system which should be used only in demo, and other pubsub system(like Redis).\n\n## Requirements\n\nPython 3.7+\n\n## Installation\n\n`pip install gql-subscriptions`\n\n> This package should be used with a network transport, for example [starlette-graphql](https://github.com/syfun/starlette-graphql)\n\n## Getting started with your first subscription\n\nTo begin with GraphQL subscriptions, start by defining a GraphQL Subscription type in your schema:\n\n```\ntype Subscription {\n    somethingChanged: Result\n}\n\ntype Result {\n    id: String\n}\n```\n\nNext, add the Subscription type to your schema definition:\n\n```\nschema {\n  query: Query\n  mutation: Mutation\n  subscription: Subscription\n}\n```\n\nNow, let\'s create a simple `PubSub` instance - it is simple pubsub implementation, based on `asyncio.Queue`.\n\n```python\nfrom gql_subscriptions import PubSub\n\npubsub = PubSub()\n```\n\nNow, implement your Subscriptions type resolver, using the `pubsub.async_iterator` to map the event you need(use [python-gql](https://github.com/syfun/python-gql)):\n\n```python\nfrom gql_subscriptions import PubSub, subscribe\n\n\npubsub = PubSub()\n\nSOMETHING_CHANGED_TOPIC = \'something_changed\'\n\n\n@subscribe\nasync def something_changed(parent, info):\n    return pubsub.async_iterator(SOMETHING_CHANGED_TOPIC)\n```\n\nNow, the GraphQL engine knows that `somethingChanged` is a subscription, and every time we use pubsub.publish over this topic - it will publish it using the transport we use:\n\n```\npubsub.publish(SOMETHING_CHANGED_TOPIC, {\'somethingChanged\': {\'id\': "123" }})\n```\n\n>Note that the default PubSub implementation is intended for demo purposes. It only works if you have a single instance of your server and doesn\'t scale beyond a couple of connections. For production usage you\'ll want to use one of the [PubSub implementations](#pubsub-implementations) backed by an external store. (e.g. Redis).\n\n## Filters\n\nWhen publishing data to subscribers, we need to make sure that each subscriber gets only the data it needs.\n\nTo do so, we can use `with_filter` decorator, which wraps the `subscription resolver` with a filter function, and lets you control each publication for each user.\n\n```\nResolverFn = Callable[[Any, Any, Dict[str, Any]], Awaitable[AsyncIterator]]\nFilterFn = Callable[[Any, Any, Dict[str, Any]], bool]\n\ndef with_filter(filter_fn: FilterFn) -> Callable[[ResolverFn], ResolverFn]\n    ...\n```\n\n`ResolverFn` is a async function which returned a `typing.AsyncIterator`.\n```\nasync def something_changed(parent, info) -> typing.AsyncIterator\n```\n\n`FilterFn` is a filter function, executed with the payload(published value), operation info, arugments, and must return bool.\n\nFor example, if `something_changed` would also accept a argument with the ID that is relevant, we can use the following code to filter according to it:\n\n```python\nfrom gql_subscriptions import PubSub, subscribe, with_filter\n\n\npubsub = PubSub()\n\nSOMETHING_CHANGED_TOPIC = \'something_changed\'\n\n\ndef filter_thing(payload, info, relevant_id):\n    return payload[\'somethingChanged\'].get(\'id\') == relevant_id\n\n\n@subscribe\n@with_filter(filter_thing)\nasync def something_changed(parent, info, relevant_id):\n    return pubsub.async_iterator(SOMETHING_CHANGED_TOPIC)\n```\n\n## Channels Mapping\n\nYou can map multiple channels into the same subscription, for example when there are multiple events that trigger the same subscription in the GraphQL engine.\n\n```python\nfrom gql_subscriptions import PubSub, subscribe, with_filter\n\npubsub = PubSub()\n\nSOMETHING_UPDATED = \'something_updated\'\nSOMETHING_CREATED = \'something_created\'\nSOMETHING_REMOVED = \'something_removed\'\n\n\n@subscribe\nasync def something_changed(parent, info):\n    return pubsub.async_iterator([SOMETHING_UPDATED, SOMETHING_CREATED, SOMETHING_REMOVED])\n```\n\n## PubSub Implementations\n\nIt can be easily replaced with some other implements of [PubSubEngine abstract class](https://github.com/syfun/gql-subscriptions/blob/master/gql_subscriptions/engine.py).\n\nThis package contains a `Redis` implements.\n\n```python\nfrom gql import subscribe\nfrom gql_subscriptions.pubsubs.redis import RedisPubSub\n\n\npubsub = RedisPubSub()\n\nSOMETHING_CHANGED_TOPIC = \'something_changed\'\n\n\n@subscribe\nasync def something_changed(parent, info):\n    return pubsub.async_iterator(SOMETHING_CHANGED_TOPIC)\n```\n\nYou can also implement a `PubSub` of your own, by using the inherit `PubSubEngine` from this package, this is a [Reids example](https://github.com/syfun/gql-subscriptions/blob/master/gql_subscriptions/pubsubs/redis.py).',
    'author': 'ysun',
    'author_email': 'sunyu418@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/syfun/gql-subscriptions',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
