import asyncio
import requests
from concurrent.futures import ThreadPoolExecutor


def fetch(session, url):
    data = {}

    try:
        with session.get(url) as response:
            data = response.text
            if response.status_code != 200:
                raise Exception(response)

    except ConnectionError as e:
        raise Exception(e)

    finally:
        return data


class APIConnector:
    def __init__(self, layer):
        self.layer = layer
        self.Session = requests.Session

        self.fetch = fetch

    async def get_data_from_iterable_source_async(self, iterable, params):
        res = []
        with ThreadPoolExecutor(max_workers=self.layer.config.max_workers) as executor:
            with self.Session() as session:
                # Set any session parameters here before calling api
                if 'verify' in params:
                    session.verify = params['verify']

                loop = asyncio.get_event_loop()
                tasks = [
                    loop.run_in_executor(
                        executor,
                        self.fetch,
                        *(session, url)
                    )
                    for url in iterable
                ]
                for response in await asyncio.gather(*tasks):
                    res.append(response)
        return res

    def get_multi_async(self, record_list=(), **params):
        loop = asyncio.get_event_loop()

        response = self.get_data_from_iterable_source_async(record_list, params)

        future = asyncio.ensure_future(response)

        return loop.run_until_complete(future)
