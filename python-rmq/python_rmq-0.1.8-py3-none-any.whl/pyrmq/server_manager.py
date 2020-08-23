import asyncio
from typing import Dict, List

import aioredis

from .connection import RedisConnection
from .consts import consts_list
from .queue import RedisQueue
from .redis_client import RedisWrapper


class ServerManager:
    def __init__(self, redis_client: RedisWrapper):
        self.redis_client = redis_client

    async def get_connections(self) -> List[str]:
        return await self.redis_client.smembers(consts_list.connections_key)

    async def get_connection_workers(self, connection_name: str) -> List[str]:
        key = consts_list.connection_consumers_template.format(connection=connection_name)
        return await self.redis_client.smembers(key)

    async def get_all_workers(self) -> Dict[str, List[str]]:
        res = {}
        connections = await self.get_connections()
        for i in connections:
            res[i] = await self.get_connection_workers(i)
        return res

    async def check_connection(self, connection_name: str) -> bool:
        key = consts_list.connection_heartbeat_template.format(connection=connection_name)
        ttl = await self.redis_client.get_ttl(key)
        return ttl > 0

    async def find_dead_connections(self) -> List[str]:
        dead_connections = []
        connections = await self.get_connections()
        for i in connections:
            if not await self.check_connection(i):
                dead_connections.append(i)
        return dead_connections

    async def clean_dead_connections(self) -> int:
        deleted = 0
        connections_list = await self.get_connections()
        for i in connections_list:
            if await self.check_connection(i):
                continue
            await self.clean_connection(i)
            deleted += 1
        return deleted

    async def clean_connection(self, connection_name: str):
        queues = await self.get_connecion_queues(connection_name)
        for i in queues:
            await self.clean_queue(i, connection_name)
        await self.redis_client.srem(consts_list.connections_key, connection_name)
        await self.redis_client.delete(consts_list.connection_queues_template.format(connection=connection_name))

    async def clean_queue(self, queue_name: str, connection_name: str):
        queue = RedisQueue(queue_name, connection_name, '', self.redis_client, asyncio.get_event_loop())
        await queue.return_all_unacked()
        await queue.close_in_connection()

    async def get_connecion_queues(self, connection_name: str) -> List[str]:
        key = consts_list.connection_queues_template.format(connection=connection_name)
        queues_list = await self.redis_client.smembers(key)
        return queues_list

    async def get_open_queues(self):
        return await self.redis_client.smembers(consts_list.queues_key)

    async def find_dead_keys(self):
        alive_connections = await self.get_connections()
        pattern = 'rmq::connection::*'
        keys = await self.redis_client.get_keys(pattern)
        res = []
        for i in keys:
            parts = i.split('::')
            connection_name = parts[2]
            if connection_name not in alive_connections:
                res.append(i)
        return res

    async def clean_dead_keys(self, keys: List[str]):
        deleted = 0
        for i in keys:
            await self.redis_client.delete(i)
            deleted += 1
        return deleted

    async def get_stats(self):
        res = {
            'connections': {},
            'queues':      {}
        }
        connections = await self.get_connections()
        for conn_name in connections:
            conn = RedisConnection(conn_name, self.redis_client, asyncio.get_event_loop())
            res['connections'][conn_name] = {
                'active': await conn.check()
            }
            is_active = await self.check_connection(conn_name)
            res['connections'][conn_name] = {
                'active':    is_active,
                'consumers': len(await self.get_connection_workers(conn_name))
            }
            queues = await self.get_open_queues()
            for b in queues:
                if b not in res['queues']:
                    queue = RedisQueue(b, conn_name, '', self.redis_client, asyncio.get_event_loop())
                    res['queues'][b] = {
                        'unacked':     await queue.unacked_count(),
                        'rejected':    await queue.rejected_count(),
                        'ready':       await queue.ready_count(),
                        'connections': 0,
                        'consumers':   0
                    }
            queues = await self.get_connecion_queues(conn_name)
            for b in queues:
                if b in res['queues']:
                    res['queues'][b]['connections'] += 1
                    res['queues'][b]['consumers'] += res['connections'][conn_name]['consumers']
        return res


async def create_manager(host: str, port: int, db: int, password: str = None) -> ServerManager:
    redis_conn = await aioredis.create_redis_pool((host, port), password=password, db=db, encoding='utf8', maxsize=1)
    await redis_conn.client_setname('rmq::server_manager')
    return ServerManager(RedisWrapper(redis_conn))
