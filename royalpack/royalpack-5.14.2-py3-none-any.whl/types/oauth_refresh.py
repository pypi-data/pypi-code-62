import aiohttp


async def oauth_refresh(*, url, client_id, client_secret, redirect_uri, refresh_code):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data={
            "client_id": client_id,
            "client_secret": client_secret,
            "code": refresh_code,
            "grant_type": "refresh_token"
        }) as response:
            j = await response.json()
            return j
