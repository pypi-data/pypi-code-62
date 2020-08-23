import asyncio

import pyrmq


async def main():
    mngr = await pyrmq.create_manager('localhost', 6379, 2)
    dead_connections = await mngr.find_dead_connections()
    if dead_connections:
        print(f'Found [{len(dead_connections)}] dead connection{"s" if len(dead_connections) > 1 else ""}. Cleaning')
        deleted = await mngr.clean_dead_connections()
        print(f'Cleaned [{deleted}] dead connection{"s" if deleted > 1 else ""}')
    else:
        print(f'No dead connections found')
    dead_keys = await mngr.find_dead_keys()
    if dead_keys:
        print(f'Found [{len(dead_keys)}] dead key{"s" if len(dead_keys) > 1 else ""}. Cleaning')
        deleted = await mngr.clean_dead_keys(dead_keys)
        print(f'Cleaned [{deleted}] dead key{"s" if deleted > 1 else ""}')
    else:
        print(f'No dead keys found')


asyncio.run(main())
