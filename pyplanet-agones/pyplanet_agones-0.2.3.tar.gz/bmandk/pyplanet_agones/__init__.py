import asyncio
import json

from pyplanet.apps.config import AppConfig
from pyplanet.contrib.command import Command
import requests
import os

class PyPlanetAgonesApp(AppConfig):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.agones_endpoint = 'http://localhost:{}'.format(os.environ['AGONES_SDK_HTTP_PORT'])
        self.health_ping_time = 5  # How much time between each health ping
        self.watcher_loop_time = 10  # How much time between checking for updates from Agones

    async def on_start(self):
        # Perms
        await self.instance.permission_manager.register('manage', 'Send Agones messages', app=self, min_level=2)

        # Commands
        await self.instance.command_manager.register(
            # Ready
            Command(command='ready', namespace='agones', target=self.command_ready,
                    perms='pyplanet_agones:manage', admin=True,
                    description='Sets the state of the server to \'Ready\' in Agones'),
            Command(command='allocate', namespace='agones', target=self.command_allocate,
                    perms='pyplanet_agones:manage', admin=True,
                    description='Allocates the server in Agones'),
            Command(command='shutdown', namespace='agones', target=self.command_shutdown,
                    perms='pyplanet_agones:manage', admin=True,
                    description='Shuts down the server via Agones'),
        )

        await self.set_ready()
        await self.health_ping()

    async def command_ready(self, player, data, **kwargs):
        await self.set_ready()

    async def command_allocate(self, player, data, **kwargs):
        await self.allocate()

    async def command_shutdown(self, player, data, **kwargs):
        await self.shutdown()

    async def set_ready(self):
        print('Setting server ready')
        endpoint = self.agones_endpoint + '/ready'
        response = await self.async_post(endpoint, json='{}')
        print(response.status_code)

        if response.status_code != 201 and response.status_code != 200:
            raise Exception('POST /ready {}'.format(response.status_code))

        await self.chat('Server is ready for a new match')

    async def allocate(self):
        print('Setting server ready')
        endpoint = self.agones_endpoint + '/allocate'
        response = await self.async_post(endpoint, json='{}')
        print(response.status_code)

        if response.status_code != 201 and response.status_code != 200:
            raise Exception('POST /allocate {}'.format(response.status_code))

        await self.chat('Server is allocated')

    async def shutdown(self):
        print('Shutting down server')
        endpoint = self.agones_endpoint + '/shutdown'
        response = await self.async_post(endpoint, json='{}')
        print(response.status_code)

        if response.status_code != 201 and response.status_code != 200:
            raise Exception('POST /shutdown {}'.format(response.status_code))

        await self.chat('Shutting down server')

    async def health_ping(self):
        endpoint = self.agones_endpoint + '/health'
        while True:
            await self.async_post(endpoint, json='{}')
            await asyncio.sleep(self.health_ping_time)

    async def agones_watcher(self):
        endpoint = self.agones_endpoint + '/watch/gameserver'

        while True:
            response = await self.async_get(endpoint, stream=True)

            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    # Which Agones events should be responded to?
                    # Yes: Server allocation with players
                    # Nice to have: Shutdown
                    print(json.loads(decoded_line))

    async def chat(self, message):
        message = '[AgonesConnector] {}'.format(message)
        self.instance.chat(message)

    # TODO: Use gRPC instead of REST, as that is preferred in Agones
    async def async_get(self, endpoint, stream=False):
        loop = asyncio.get_event_loop()
        future = loop.run_in_executor(None, requests.get, endpoint, stream)
        return await future

    async def async_post(self, endpoint, json):
        loop = asyncio.get_event_loop()
        future = loop.run_in_executor(None, requests.post, endpoint, json)
        return await future
