import asyncio
import os

from .connection import RedisConnection, open_connection
from .consumer import Consumer
from .delivery import Delivery
from .queue import RedisQueue
from .server_manager import create_manager

try:
    import uvloop
except ImportError:
    uvloop = None
else:
    if 'DISABLE_UVLOOP' not in os.environ:
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

__version__ = '0.1.8'
