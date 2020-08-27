import pytest
import asyncio
from . import util


@pytest.fixture
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop


def test_util_basic(event_loop):
    vertical = [1, 2]
    horizontal = [3, 4]

    def func(vertial, horizontal):
        r = [[0 for j in range(0, len(horizontal))] for i in range(0, len(vertical))]
        for i in range(0, len(vertical)):
            for j in range(0, len(horizontal)):
                r[i][j] = vertical[i] * horizontal[j]
        return r
    result = event_loop.run_until_complete(util.table_split(vertical, horizontal, func))
    assert result[0][0] == 3
    assert result[0][1] == 4
    assert result[1][0] == 6
    assert result[1][1] == 8


def test_util_large(event_loop):
    vertical = [i for i in range(0, 1000)]
    horizontal = [i for i in range(0, 2000)]

    async def func(vertial, horizontal):
        r = [[0 for j in range(0, len(horizontal))] for i in range(0, len(vertical))]
        for i in range(0, len(vertical)):
            for j in range(0, len(horizontal)):
                r[i][j] = vertical[i] * horizontal[j]
        return r
    result = event_loop.run_until_complete(util.table_split(vertical, horizontal, func))
    for i in range(0, len(vertical)):
        for j in range(0, len(horizontal)):
            assert result[i][j] == vertical[i] * horizontal[j]
