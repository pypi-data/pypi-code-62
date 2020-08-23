import asyncio
from typing import List

import aioredis

from .consts import consts_list
from .misc import randomword
from .queue import RedisQueue
from .redis_client import RedisWrapper

HEARTBEAT_DURATION = 60
HEARTBEAT_INTERVAL = HEARTBEAT_DURATION / 2


class RedisConnection:
    name: str
    heartbeat_key: str
    queues_key: str
    redis_client: RedisWrapper
    heartbeat_stopped: bool
    started_connection: bool

    def __init__(self, tag: str, redis_client: RedisWrapper, ioloop: asyncio.AbstractEventLoop):
        if '::' in tag:
            raise ValueError('You cannot use :: in connection\'s tag')
        name = f'{tag}-{randomword(6)}'
        self.name = name
        self.heartbeat_key = consts_list.connection_heartbeat_template.format(connection=name)
        self.queues_key = consts_list.connection_queues_template.format(connection=name)
        self.redis_client = redis_client
        self.heartbeat_stopped = False
        self.started_connection = False
        self.ioloop = ioloop

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    async def start_connection(self):
        heartbeat_result = await self.update_heartbeat()
        if not heartbeat_result:
            raise ConnectionError(f'rmq connection failed to update heartbeat {self}')
        await self.redis_client.sadd(consts_list.connections_key, self.name)
        asyncio.create_task(self.heartbeat())
        self.started_connection = True

    async def open_queue(self, name: str) -> RedisQueue:
        if not self.started_connection:
            raise ConnectionError(f'Connection wasn\'t activated {self}. Use start_connection first')
        await self.redis_client.sadd(consts_list.queues_key, name)
        queue = RedisQueue(name, self.name, self.queues_key, self.redis_client, self.ioloop)
        return queue

    async def get_connections(self):
        return self.redis_client.smembers(consts_list.connections_key)

    async def check(self) -> bool:
        ttl = await self.redis_client.get_ttl(self.heartbeat_key)
        return ttl > 0

    async def stop_heartbeat(self) -> int:
        self.heartbeat_stopped = True
        return await self.redis_client.delete(self.heartbeat_key)

    async def close(self) -> int:
        if not self.started_connection:
            raise ConnectionError(f'Connection wasn\'t activated {self}. Use start_connection first')
        return await self.redis_client.srem(consts_list.connections_key, self.name)

    async def get_open_queues(self) -> List[str]:
        return await self.redis_client.smembers(consts_list.queues_key)

    async def close_all_queues(self) -> int:
        if not self.started_connection:
            raise ConnectionError(f'Connection wasn\'t activated {self}. Use start_connection first')
        return await self.redis_client.delete(consts_list.queues_key)

    async def close_all_queues_in_connection(self):
        if not self.started_connection:
            raise ConnectionError(f'Connection wasn\'t activated {self}. Use start_connection first')
        await self.redis_client.delete(self.queues_key)

    async def get_consuming_queues(self) -> List[str]:
        return await self.redis_client.smembers(self.queues_key)

    async def heartbeat(self):
        while True:
            update_result = await self.update_heartbeat()
            if not update_result:
                pass
            await asyncio.sleep(HEARTBEAT_INTERVAL)
            if self.heartbeat_stopped:
                return

    async def update_heartbeat(self):
        return await self.redis_client.set(self.heartbeat_key, 1, HEARTBEAT_DURATION)


async def open_connection(tag: str, host: str, port: int, db: int, password: str = None) -> RedisConnection:
    redis_conn = await aioredis.create_redis_pool((host, port), password=password, db=db, encoding='utf8')
    return open_connection_with_redis_client(tag, redis_conn)


def open_connection_with_redis_client(tag, redis_client: aioredis.Redis) -> RedisConnection:
    return RedisConnection(tag, RedisWrapper(redis_client), asyncio.get_event_loop())
