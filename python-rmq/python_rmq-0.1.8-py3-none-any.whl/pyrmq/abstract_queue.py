import abc

from .consumer import Consumer


class Queue(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def publish(self, payload: str):
        pass

    @abc.abstractmethod
    async def publish_bytes(self, payload: bytes):
        pass

    @abc.abstractmethod
    async def set_push_queue(self, push_queue: 'Queue'):
        pass

    @abc.abstractmethod
    async def start_consuming(self, prefetch_limit: int, poll_duration: int):
        pass

    @abc.abstractmethod
    async def stop_consuming(self):
        pass

    @abc.abstractmethod
    async def add_consumer(self, tag: str, consumer: Consumer):
        pass

    @abc.abstractmethod
    async def purge_ready(self) -> int:
        pass

    @abc.abstractmethod
    async def purge_rejected(self) -> int:
        pass

    @abc.abstractmethod
    async def return_all_rejected(self) -> int:
        pass

    @abc.abstractmethod
    async def close(self):
        pass
