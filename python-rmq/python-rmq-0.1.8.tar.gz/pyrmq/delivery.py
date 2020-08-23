from .redis_client import RedisWrapper


class Delivery:
    payload: str
    unacked_key: str
    rejected_key: str
    push_key: str
    redis_client: RedisWrapper

    def __init__(self, payload: str, unacked_key: str, rejected_key: str, push_key: str, redis_client: RedisWrapper):
        self.payload = payload
        self.unacked_key = unacked_key
        self.rejected_key = rejected_key
        self.push_key = push_key
        self.redis_client = redis_client

    def __repr__(self):
        return f'[{self.payload} {self.unacked_key}]'

    def __str__(self):
        return f'[{self.payload} {self.unacked_key}]'

    @property
    def payload(self):
        return self._payload

    @payload.setter
    def payload(self, value):
        self._payload = value

    async def ack(self) -> bool:
        count = await self.redis_client.lrem(self.unacked_key, 1, self.payload)
        return count == 1

    async def reject(self):
        await self._move(self.rejected_key)

    async def push(self):
        if self.push_key:
            await self._move(self.push_key)
        else:
            await self._move(self.rejected_key)

    async def _move(self, key: str):
        await self.redis_client.lpush(key, self.payload)
        await self.redis_client.lrem(self.unacked_key, 1, self.payload)
