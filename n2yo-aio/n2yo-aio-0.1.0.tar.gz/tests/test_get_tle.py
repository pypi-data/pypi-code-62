import asyncio

import pytest

from n2yo.n2yo import N2YO


@pytest.mark.asyncio
async def test_get_tle():
    n2yo = N2YO(api_key='XM2S6V-3Z2NV5-GDJDKJ-4J98')
    info, tle = await n2yo.get_tle(25544)
    assert info['satid'] == 25544


if __name__ == '__main__':
    asyncio.run(test_get_tle())
