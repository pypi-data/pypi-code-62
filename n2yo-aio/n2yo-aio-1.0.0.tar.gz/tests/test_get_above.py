import asyncio

import pytest

from n2yo.n2yo import N2YO
from n2yo.satellite_categories import N2YOSatelliteCategory


@pytest.mark.asyncio
async def test_get_above():
    n2yo = N2YO(
        api_key='XM2S6V-3Z2NV5-GDJDKJ-4J98',
        latitude=45.4642, longitude=9.1900, altitude=0
    )
    info, above = await n2yo.get_above(category_id=N2YOSatelliteCategory.Amateur)
    assert info['category'] == 'Amateur radio'


if __name__ == '__main__':
    asyncio.run(test_get_above())
