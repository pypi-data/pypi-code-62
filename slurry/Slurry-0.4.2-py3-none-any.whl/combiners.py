"""Pipeline sections for combining multiple inputs into a single output."""
import builtins
import itertools
from typing import Any, AsyncIterable, Sequence, Union

import trio
from async_generator import aclosing

from .abc import Section

class Chain(Section):
    """Chains asynchronous sequences.

    Outputs items from each source in turn, until it is exhausted. If a source never reaches the
    end, remaining sources will not be iterated.

    Chain can be placed as a middle section and will chain the input of the previous section.

    .. Note::
        By default, the input is added as the first source. If the input is added last instead
        of first, it will cause backpressure to be applied upstream.

    :param sources: One or more async iterables that will be chained together.
    :type sources: Sequence[AsyncIterable[Any]]
    :param place_input: Iteration priority of the pipeline input source. Options:
        ``'first'`` (default) \| ``'last'``.
    :type place_input: string
    """
    def __init__(self, *sources: Sequence[AsyncIterable[Any]], place_input='first'):
        super().__init__()
        self.sources = sources
        self.place_input = _validate_place_input(place_input)

    async def pump(self, input, output):
        if input is not None:
            if self.place_input == 'first':
                sources = (input, *self.sources)
            elif self.place_input == 'last':
                sources = (*self.sources, input)
        else:
            sources = self.sources
        async with output:
            for source in sources:
                async with aclosing(source) as agen:
                    async for item in agen:
                        await output.send(item)

class Merge(Section):
    """Merges asynchronous sequences or pipeline sections.

    Sources are iterated in parallel and items are send from each source, as soon as
    they become available.

    If Merge is used as a middle section, the input will be added to the sources.

    Sources can be pipeline sections, which will be treated as first sections, with
    no input. Merge will take care of running the pump task for these sections.

    :param sources: One or more async iterables or sections who's contents will be merged.
    :type sources: Sequence[Union[AsyncIterable[Any], Section]]
    """
    def __init__(self, *sources: Sequence[Union[AsyncIterable[Any], Section]]):
        super().__init__()
        self.sources = sources

    async def pump(self, input, output):
        if input is not None:
            sources = (input, *self.sources)
        else:
            sources = self.sources
        async with output, trio.open_nursery() as nursery:

            async def pull_task(source, output):
                if isinstance(source, Section):
                    send_channel, receive_channel = trio.open_memory_channel(0)
                    nursery.start_soon(source.pump, None, send_channel)
                    source = receive_channel
                async with output, aclosing(source) as aiter:
                    async for item in aiter:
                        await output.send(item)

            for source in sources:
                nursery.start_soon(pull_task, source, output.clone())

class Zip(Section):
    """Zip asynchronous sequences.

    Sources are iterated in parallel and as soon as all sources have an item available, those
    items are output as a tuple.

    Zip can be used as a middle section, and the pipeline input will be added to the sources.

    .. Note::
        If sources are out of sync, the fastest source will have to wait for the slowest, which
        will cause backpressure.

    :param sources:  One or more async iterables, who's contents will be zipped.
    :type sources: Sequence[AsyncIterable[Any]]
    :param place_input:  Position of the pipeline input source in the output tuple. Options:
        ``'first'`` (default) \| ``'last'``.
    :type place_input: string
    """
    def __init__(self, *sources: Sequence[AsyncIterable[Any]], place_input='first'):
        super().__init__()
        self.sources = sources
        self.place_input = _validate_place_input(place_input)

    async def pump(self, input, output):
        if input is not None:
            if self.place_input == 'first':
                sources = (input, *self.sources)
            elif self.place_input == 'last':
                sources = (*self.sources, input)
        else:
            sources = self.sources

        async with output:
            with trio.CancelScope() as cancel_scope:
                async def pull_task(source, results, index):
                    try:
                        results[index] = await source.__anext__()
                    except StopAsyncIteration:
                        cancel_scope.cancel()

                while True:
                    results = [None for _ in sources]
                    async with trio.open_nursery() as nursery:
                        for i, source in builtins.enumerate(sources):
                            nursery.start_soon(pull_task, source, results, i)
                    await output.send(tuple(results))

class ZipLatest(Section):
    """Zips asynchronous sequences and outputs a result on every received item.

    Sources are iterated in parallel and a tuple is output each time a result is ready
    on any source. The tuple values will be the last received value from each source.

    Using the monitor argument, one or more asynchronous sequences can be added with the property
    that they will not trigger an output by themselves. Their latest value will be stored and
    added to the output value, but will only be output if a new item arrives at one of the main
    sources.

    ZipLatest can be used as a middle section, in which case the upstream pipeline is
    added as an input.

    .. Note::
        If any single source is exchausted, all remaining sources will be forcibly closed, and
        the pipeline will stop.

    :param sources: One or more async iterables that will be zipped together.
    :type sources: Sequence[AsyncIterable[Any]]
    :param partial: If ``True`` (default) output will be sent as soon as the first input arrives.
        Otherwise, all main sources must send at least one item, before an output is generated.
    :type partial: bool
    :param default: If the parameter ``partial`` is ``True``, this value is used as the
        default value to output, until an input has arrived on a source. Defaults to ``None``.
    :type default: Any
    :param monitor: Additional asynchronous sequences to monitor.
    :type monitor: Optional[Union[AsyncIterable[Any], Sequence[AsyncIterable[Any]]]]
    :param place_input: Position of the pipeline input source in the output tuple. Options:
        ``'first'`` (default)|``'last'``
    :type place_input: string
    :param monitor_input: Input is used as a monitored stream instead of a main source.
        Defaults to ``False``
    :type monitor_input: bool
    """
    def __init__(self, *sources: Sequence[AsyncIterable[Any]],
                 partial=True,
                 default=None,
                 monitor=(),
                 place_input='first',
                 monitor_input=False):
        super().__init__()
        self.sources = sources
        self.partial = partial
        self.default = default
        self.monitor = monitor
        self.place_input = _validate_place_input(place_input)
        self.monitor_input = monitor_input

    async def pump(self, input, output):
        sources = self.sources
        try:
            iter(self.monitor)
            monitor = self.monitor
        except TypeError:
            monitor = (self.monitor,)

        if input is not None:
            if self.monitor_input:
                if self.place_input == 'first':
                    monitor = (input, *monitor)
                elif self.place_input == 'last':
                    monitor = (*monitor, input)
            else:
                if self.place_input == 'first':
                    sources = (input, *sources)
                elif self.place_input == 'last':
                    sources = (*sources, input)

        results = [self.default for _ in itertools.chain(sources, monitor)]
        ready = [False for _ in results]

        async with output, trio.open_nursery() as nursery:

            async def pull_task(index, source, monitor=False):
                async with aclosing(source) as aiter:
                    async for item in aiter:
                        results[index] = item
                        ready[index] = True
                        if not monitor and (self.partial or False not in ready):
                            await output.send(tuple(results))
                nursery.cancel_scope.cancel()

            for i, source in builtins.enumerate(sources):
                nursery.start_soon(pull_task, i, source)
            for i, source in builtins.enumerate(monitor):
                nursery.start_soon(pull_task, i + len(sources), source, True)

def _validate_place_input(place_input):
    if isinstance(place_input, str):
        if place_input not in ['first', 'last']:
            raise ValueError(f'Invalid place_input argument: {place_input}')
    else:
        raise TypeError('place_input argument has invalid type.')
    return place_input
