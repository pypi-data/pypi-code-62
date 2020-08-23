from typing import List, Optional

import aioredis


class RedisWrapper:
    def __init__(self, redis_client: aioredis.Redis):
        self.raw_client: aioredis.Redis = redis_client

    async def set(self, key: str, value: str, expiration: int) -> bool:
        return await self.raw_client.set(key, value, expire=expiration)

    async def delete(self, key: str) -> int:
        return await self.raw_client.delete(key)

    async def get_ttl(self, key: str):
        r = int(await self.raw_client.ttl(key))
        return int(r)

    async def lpush(self, key: str, value: str):
        await self.raw_client.lpush(key, value)

    async def llen(self, key: str) -> int:
        r = await self.raw_client.llen(key)
        return int(r)

    async def lrem(self, key: str, count: int, value: str) -> int:
        r = await self.raw_client.lrem(key, count, value)
        return int(r)

    async def ltrim(self, key: str, start: int, stop: int):
        await self.raw_client.ltrim(key, start, stop)

    async def rpoplpush(self, source: str, destination: str) -> Optional[str]:
        r = await self.raw_client.rpoplpush(source, destination)
        return str(r) if r is not None else None

    async def sadd(self, key: str, value: str):
        await self.raw_client.sadd(key, value)

    async def smembers(self, key: str) -> List[str]:
        r = await self.raw_client.smembers(key, encoding='utf8')
        return list(r)

    async def srem(self, key: str, value: str) -> int:
        r = await self.raw_client.srem(key, value)
        return int(r)

    async def flush_db(self):
        await self.raw_client.flushdb()

    async def get_keys(self, pattern: str) -> List[str]:
        res = []
        cur = b'0'
        while cur:
            cur, keys = await self.raw_client.scan(cur, match=pattern)
            if keys:
                res.extend(keys)
        return res
