#!/usr/bin/env python3

import asyncio
import signal
import sys

from oort.shared.config import get_logger
from .preparator import UploadPreparator
from .uploader import FileUploader

MAX_TASKS = 3


class UploadScheduler(object):
    def __init__(self):
        signal.signal(signal.SIGINT, self.signal_handler)  # register the signal with the signal handler first
        self._logger = get_logger()
        self._loop = asyncio.get_event_loop()

        # Creating a single async Queue
        self._queue = asyncio.Queue(0, loop=self._loop)

        # Creating a limited number of consumers to avoid too many simultaneous call to api.arcsecond.io
        # Somehow, one must use asyncio.ensure_future instead of create_task, despite documentation.
        # See https://stackoverflow.com/a/57026514/707984
        # See also https://www.codependentcodr.com/asyncio-you-are-a-complex-beast.html
        self._consumers = [asyncio.ensure_future(self._consumer(self._queue)) for _ in range(MAX_TASKS)]

    def __del__(self):
        self._cleanup()

    def _cleanup(self):
        for _consumer in self._consumers:
            _consumer.cancel()
        self._loop.stop()
        self._loop.close()

    def signal_handler(self, signum, frame):
        print('Cleaning up consumer tasks before exiting...')
        signal.signal(signum, signal.SIG_IGN)  # ignore additional signals
        self._cleanup()
        sys.exit(0)

    async def _consumer(self, queue):
        while True:
            preparator: UploadPreparator = await queue.get()
            await preparator.prepare()
            if preparator.dataset:
                file_uploader = FileUploader(preparator.pack, preparator.identity, preparator.dataset)
                await file_uploader.upload()
            else:
                self._logger.info(f'Missing dataset, upload skipped for {preparator.pack.file_path}')
            self._logger.info(f'Async upload task done. {len(self._consumers)}')
            queue.task_done()

    async def _producer(self, preparator: UploadPreparator):
        await self._queue.put(preparator)

    def prepare_and_upload(self, preparator: UploadPreparator):
        self._logger.info('Queuing async upload task...')
        self._loop.run_until_complete(self._producer(preparator))


scheduler = UploadScheduler()
