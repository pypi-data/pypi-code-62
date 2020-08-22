"""Pipeline sections with age- and volume-based buffers."""
from collections import deque
import math
from typing import Any, AsyncIterable, Callable, Optional, Sequence

import trio
from async_generator import aclosing

from .abc import Section

class Window(Section):
    """Window buffer with size and age limits.

    ``Window`` iterates an asynchronous sequence and stores each received item in a
    buffer. Each time another item is received, the buffer is filtered by dumping the oldest items
    first, until the configured window conditions for the buffer size and item age are satisfied.
    After filtering, the whole buffer is output as a tuple, with the oldest item first, and the
    newest item last.

    .. Note::
        Items are added to the right side and are removed from the left side of the buffer.

        All items remain in the buffer, unless they are removed by one of the window
        conditions and any item can be output more than once.

    :param max_size: The maximum buffer size.
    :type max_size: int
    :param source: Input when used as first section.
    :type source: Optional[AsyncIterable[Any]]
    :param max_age: Maximum item age in seconds. (default: unlimited)
    :type max_age: float
    :param min_size: Minimum amount of items in the buffer to trigger an output.
    :type min_size: int
    """
    def __init__(self, max_size: int, source: Optional[AsyncIterable[Any]] = None, *,
                 max_age: float = math.inf,
                 min_size: int = 1):
        super().__init__()
        self.source = source
        self.max_size = max_size
        self.max_age = max_age
        self.min_size = min_size

    async def pump(self, input, output):
        if input is None:
            if self.source is not None:
                input = self.source
            else:
                raise RuntimeError('No input provided.')
        buf = deque()
        async with aclosing(input) as aiter, output:
            async for item in aiter:
                now = trio.current_time()
                buf.append((item, now))
                while len(buf) > self.max_size or now - buf[0][1] > self.max_age:
                    buf.popleft()
                if len(buf) >= self.min_size:
                    await output.send(tuple(i[0] for i in buf))

class Group(Section):
    """Groups received items by time based interval.

    Group awaits an item to arrive from source, adds it to a buffer and sets a timer based on
    the ``interval`` parameter. While the timer is active, additional items received are added
    to the buffer. When the timer runs out, or if the buffer size equals ``max_size``, the buffer
    is sent down the pipeline and a new empty buffer is created.

    .. Note::
        The buffer is not sent at regular intervals. The timer is triggered when an item is
        is received into an empty buffer.

        An output buffer will always contain at least one item.

    The items in the buffer can optionally be mapped over, by supplying a mapper function and be
    reduced to a single value, by supplying a reducer function.

    :param interval: Time in seconds from when an item arrives until the buffer is sent.
    :type interval: float
    :param source: Input when used as first section.
    :type source: Optional[AsyncIterable[Any]]
    :param max_size: Maximum number of items in buffer, which when reached, will cause the buffer
        to be sent.
    :type max_size: int
    :param mapper: Optional mapping function used to transform each received item.
    :type mapper: Optional[Callable[[Any], Any]]
    :param reducer: Optional reducer function used to transform the buffer to a single value.
    :type reducer: Optional[Callable[[Sequence[Any]], Any]]
    """
    def __init__(self, interval: float, source: Optional[AsyncIterable[Any]] = None, *,
                 max_size: int = math.inf,
                 mapper: Optional[Callable[[Any], Any]] = None,
                 reducer: Optional[Callable[[Sequence[Any]], Any]] = None):
        super().__init__()
        self.source = source
        self.interval = interval
        self.max_size = max_size
        self.mapper = mapper
        self.reducer = reducer

    async def pump(self, input, output):
        if input is None:
            if self.source is not None:
                input = self.source
            else:
                raise RuntimeError('No input provided.')
        async with output, aclosing(input) as aiter:
            while True:
                buffer = []
                try:
                    self._add_item(await aiter.__anext__(), buffer)
                    with trio.move_on_after(self.interval):
                        while True:
                            if len(buffer) == self.max_size:
                                break
                            self._add_item(await aiter.__anext__(), buffer)
                except StopAsyncIteration:
                    if buffer:
                        await output.send(self._process_result(buffer))
                    break
                await output.send(self._process_result(buffer))

    def _add_item(self, item, buffer):
        if self.mapper is not None:
            buffer.append(self.mapper(item))
        else:
            buffer.append(item)

    def _process_result(self, buffer):
        if self.reducer is not None:
            return self.reducer(buffer)
        return tuple(buffer)

class Delay(Section):
    """Delays transmission of each item received by an interval.

    Received items are temporarily stored in an unbounded queue, along with a timestamp, using
    a background task. The foreground task takes items from the queue, and waits until the
    item is older than the given interval and then transmits it.

    :param interval: Number of seconds that each item is delayed.
    :type interval: float
    :param source: Input when used as first section.
    :type source: Optional[AsyncIterable[Any]]
    """
    def __init__(self, interval: float, source: Optional[AsyncIterable[Any]] = None):
        super().__init__()
        self.source = source
        self.interval = interval

    async def pump(self, input, output):
        if input is None:
            if self.source is not None:
                input = self.source
            else:
                raise RuntimeError('No input provided.')
        buffer_input_channel, buffer_output_channel = trio.open_memory_channel(math.inf)

        async def pull_task():
            async with buffer_input_channel, aclosing(input) as aiter:
                async for item in aiter:
                    await buffer_input_channel.send((item, trio.current_time() + self.interval))

        async with trio.open_nursery() as nursery:
            nursery.start_soon(pull_task)
            async with buffer_output_channel, output:
                async for item, timestamp in buffer_output_channel:
                    now = trio.current_time()
                    if timestamp > now:
                        await trio.sleep(timestamp - now)
                    await output.send(item)

class RateLimit(Section):
    """Limits data rate of an input to a certain interval.

    The first item received is transmitted and triggers a timer. Any other items received while
    the timer is active are discarded. After the timer runs out, the cycle can repeat.

    :param interval: Minimum number of seconds between each sent item.
    :type interval: float
    :param source: Input when used as first section.
    :type source: Optional[AsyncIterable[Any]]
    """
    def __init__(self, interval, source=None):
        super().__init__()
        self.source = source
        self.interval = interval

    async def pump(self, input, output):
        if self.source is not None:
            input = self.source
        then = 0
        async with aclosing(input) as aiter, output:
            async for item in aiter:
                now = trio.current_time()
                if now - then > self.interval:
                    then = now
                    await output.send(item)
