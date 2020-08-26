import asyncio

import pytest

from n2yo.n2yo import N2YO


@pytest.mark.asyncio
async def test_get_satellite_positions():
    n2yo = N2YO(
        api_key='XM2S6V-3Z2NV5-GDJDKJ-4J98',
        latitude=45.4642, longitude=9.1900, altitude=0
    )
    info, ans = await n2yo.get_satellite_positions(25544, 60)
    assert info['satid'] == 25544


if __name__ == '__main__':
    asyncio.run(test_get_satellite_positions())
