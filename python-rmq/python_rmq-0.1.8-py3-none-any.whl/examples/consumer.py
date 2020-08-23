import asyncio
import time

import pyrmq

batch_size = 100
consumers_amount = 10
proceeded_count = 0
prev_count = 0


class NewConsumer(pyrmq.Consumer):
    started = time.time()
    proceeded_count = 0

    def __init__(self, name: str):
        self.name = name
        print(self.name)

    async def consume(self, delivery: pyrmq.Delivery):
        self.proceeded_count += 1
        # await asyncio.sleep(.02)
        await delivery.ack()
        if self.proceeded_count % batch_size == 0:
            diff = time.time() - self.started
            self.started = time.time()
            per_second = int(1 / (diff / batch_size))
            print(f'[{self.name}]-{per_second}/second')


def create_new_consumer(name: str) -> NewConsumer:
    return NewConsumer(f'consumer-{name + 1}')


async def main():
    conn = await pyrmq.open_connection('consumer', 'localhost', 6379, 2)
    await conn.start_connection()
    things = await conn.open_queue('things')
    await things.return_all_unacked()
    await things.start_consuming(1000, 1)
    await things.remove_all_consumers()
    for i in range(consumers_amount):
        await things.add_consumer(f'consumer-{i}', create_new_consumer(i))


asyncio.get_event_loop().create_task(main())
asyncio.get_event_loop().run_forever()
