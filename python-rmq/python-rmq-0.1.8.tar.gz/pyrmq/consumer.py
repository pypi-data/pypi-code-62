import abc

from .delivery import Delivery


class Consumer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def consume(self, delivery: Delivery):
        pass
