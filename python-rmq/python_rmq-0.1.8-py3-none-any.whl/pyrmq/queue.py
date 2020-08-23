import asyncio
from typing import List, Optional

from loguru import logger

from .abstract_queue import Queue
from .consts import consts_list
from .consumer import Consumer
from .delivery import Delivery
from .misc import randomword
from .redis_client import RedisWrapper


class RedisQueue(Queue):
    name: str
    connection_name: str
    queues_key: str
    consumers_key: str
    ready_key: str
    rejected_key: str
    unacked_key: str
    push_key: str
    redis_client: RedisWrapper
    prefetch_limit: int
    poll_duration: float
    consuming_stopped: bool
    delivery_queue: Optional[asyncio.Queue]

    def __init__(self, tag: str, connection_name: str, queues_key: str, redis_client: RedisWrapper,
                 event_loop: asyncio.AbstractEventLoop):
        name = tag
        self.name = name
        self.connection_name = connection_name
        self.queues_key = queues_key
        self.consumers_key = consts_list.connection_queue_consumers_template.format(connection=connection_name,
                                                                                    queue=name)
        self.ready_key = consts_list.queue_ready_template.format(queue=name)
        self.rejected_key = consts_list.queue_rejected_template.format(queue=name)
        self.unacked_key = consts_list.connection_queue_unacked_template.format(connection=connection_name, queue=name)
        self.connection_consumers_key = consts_list.connection_consumers_template.format(connection=connection_name)
        self.push_key: str = ''
        self.redis_client = redis_client
        self.delivery_queue = None
        self.consuming_stopped = True
        self.ioloop = event_loop
        self._consumers: List[Consumer] = []
        self._last_consumer_id = 0

    def __repr__(self):
        return f'[{self.name} conn:{self.connection_name}]'

    def __str__(self):
        return f'[{self.name} conn:{self.connection_name}]'

    async def publish(self, payload: str):
        await self.redis_client.lpush(self.ready_key, payload)

    async def publish_bytes(self, payload: bytes):
        stringified_bytes = payload.decode('utf8')
        await self.publish(stringified_bytes)

    async def purge_ready(self) -> int:
        return await self._delete_redis_list(self.ready_key)

    async def purge_rejected(self) -> int:
        return await self._delete_redis_list(self.rejected_key)

    async def _delete_redis_list(self, key: str) -> int:
        list_length = await self.redis_client.llen(key)
        if list_length == 0:
            return 0
        todo = list_length
        while todo > 0:
            batch_size = consts_list.purge_batch_size
            if batch_size > todo:
                batch_size = todo
            await self.redis_client.ltrim(key, 0, -1 - batch_size)
            todo -= consts_list.purge_batch_size
        return list_length

    async def close(self) -> bool:
        await self.purge_rejected()
        await self.purge_ready()
        count = await self.redis_client.srem(consts_list.queues_key, self.name)
        return count > 0

    async def ready_count(self) -> int:
        return await self.redis_client.llen(self.ready_key)

    async def unacked_count(self) -> int:
        return await self.redis_client.llen(self.unacked_key)

    async def rejected_count(self) -> int:
        return await self.redis_client.llen(self.rejected_key)

    async def return_all_unacked(self) -> int:
        return await self._move(self.unacked_key, self.ready_key)

    async def return_all_rejected(self) -> int:
        return await self._move(self.rejected_key, self.ready_key)

    async def _move(self, source: str, destination: str) -> int:
        count = await self.redis_client.llen(source)
        if not count:
            return 0
        moved_count = count
        for i in range(0, moved_count):
            key = await self.redis_client.rpoplpush(source, destination)
            if key is None:
                return i
        return moved_count

    async def set_push_queue(self, push_queue: 'RedisQueue'):
        self.push_key = push_queue.ready_key

    async def close_in_connection(self):
        await self.redis_client.delete(self.unacked_key)
        await self.redis_client.delete(self.consumers_key)
        await self.redis_client.srem(self.queues_key, self.name)

    async def start_consuming(self, prefetch_limit: int, poll_duration: float) -> bool:
        if self.delivery_queue is not None:
            return False
        await self.redis_client.sadd(self.queues_key, self.name)
        self.prefetch_limit = prefetch_limit
        self.poll_duration = poll_duration
        self.delivery_queue = asyncio.Queue(maxsize=prefetch_limit)
        self.consuming_stopped = False
        self.ioloop.create_task(self._consume())

    async def stop_consuming(self):
        if self.delivery_queue is None or self.consuming_stopped:
            return
        self.consuming_stopped = True

    async def _consume(self):
        while True:
            batch_size = await self._batch_size()
            want_more = await self._consume_batch(batch_size)
            if not want_more:
                await asyncio.sleep(self.poll_duration)
            if self.consuming_stopped:
                await self.delivery_queue.join()
                self.delivery_queue = None
                return

    async def _batch_size(self):
        prefetch_limit = self.prefetch_limit - await self.unacked_count()
        ready_count = await self.ready_count()
        res = prefetch_limit
        if ready_count < res:
            res = ready_count
        if self.delivery_queue.full():
            res = 0
        else:
            pre_res = self.delivery_queue.maxsize - self.delivery_queue.qsize()
            if res > pre_res:
                res = pre_res
        return res

    async def _consume_batch(self, batch_size: int) -> bool:
        if batch_size == 0:
            return False
        for i in range(0, batch_size):
            value = await self.redis_client.rpoplpush(self.ready_key, self.unacked_key)
            if value is None:
                return False
            new_delivery = Delivery(value, self.unacked_key, self.rejected_key, self.push_key, self.redis_client)
            await self.delivery_queue.put(new_delivery)
        return True

    async def add_consumer(self, tag: str, consumer: Consumer) -> str:
        name = await self._add_consumer(tag)
        self._consumers.append(consumer)
        if len(self._consumers) == 1:
            self.ioloop.create_task(self._consumer_consume())
        return name

    async def _add_consumer(self, tag: str):
        if self.delivery_queue is None:
            logger.error(f'rmq queue failed to add consumer, call start_consuming first! {self}')
        name = f'{tag}-{randomword(6)}'
        await self.redis_client.sadd(self.consumers_key, name)
        await self.redis_client.sadd(self.connection_consumers_key, name)
        return name

    async def remove_all_consumers(self) -> int:
        return await self.redis_client.delete(self.consumers_key)

    async def get_all_consumers(self) -> List[str]:
        return await self.redis_client.smembers(self.consumers_key)

    async def _consumer_consume(self):
        while True:
            if self.delivery_queue is not None:
                delivery = await self.delivery_queue.get()
                tasks = [self._on_delivery(delivery)]
                await asyncio.gather(*tasks)

    async def _on_delivery(self, delivery: Delivery):
        if self._last_consumer_id >= len(self._consumers) - 1:
            consumer_id = 0
        else:
            consumer_id = self._last_consumer_id + 1
        self._last_consumer_id = consumer_id
        consumer = self._consumers[consumer_id]
        await consumer.consume(delivery=delivery)
