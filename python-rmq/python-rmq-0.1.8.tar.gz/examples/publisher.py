import asyncio
import time

import pyrmq

deliveries = 1_000_000
batch_size = 10_000


async def main():
    conn = await pyrmq.open_connection('producer', 'localhost', 6379, 11)
    await conn.start_connection()
    things = await conn.open_queue('things')
    before = time.time()
    for i in range(deliveries):
        delivery_body = f'delivery #{i}'
        await things.publish(delivery_body)
        if i % batch_size == 0 and i != 0:
            diff = time.time() - before
            before = time.time()
            per_second = 1 / (diff / batch_size)
            print(f'produced #{i} #{delivery_body} #{per_second}')


asyncio.run(main())
