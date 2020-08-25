#
# Copyright (c) 2019 Andreas Oberritter
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

import asyncio
import logging
from urllib.parse import urlparse
from async_timeout import timeout
import serial
from serial import SerialException
from serial_asyncio import create_serial_connection
from .vpackets import *
from scapy.packet import Raw

logger = logging.getLogger(__name__)

class ViessmannProtocol(asyncio.Protocol):
    _ACK = 0x06
    _START_BYTE = 0x41
    _PERIODIC_WORD = 0x05
    _END_COMMUNICATION = b"\x04"
    _PING = b"\x16\x00\x00"
    _BAUD_RATE = 4800

    def __init__(self, url):
        super().__init__()
        self._url = urlparse(url)
        self._transport = None
        self._loop = None
        self._running = False
        self._connecting = False
        self._buf = b''
        self._lock = None
        self._ack_event = asyncio.Event()
        self._periodic_event = asyncio.Event()
        self._message_event = asyncio.Event()
        self._pkt = None

    def data_received(self, data: bytes):
        self._buf += data
        logger.debug("BUF:")
        logger.debug(self._buf)
        if self._buf[0] == self._ACK:
            self._ack_event.set()
            self._buf = self._buf[1:]
        elif self._buf[0] == self._PERIODIC_WORD:
            if self._connecting:
                self._buf = self._buf[1:]
                self._connecting = False
                self._periodic_event.set()
            else:
                logger.warning("received a periodic byte. Reconnecting")
                self._buf = b''
                if self._running and not self._lock.locked():
                    asyncio.ensure_future(self._reconnect(), loop=self._loop)
        elif self._buf[0] == self._START_BYTE:
            if len(self._buf) < 3:
                return

            length = self._buf[1]
            if len(self._buf) < length+3:
                return

            msg_bytes, self._buf = self._buf[:length+3], self._buf[length+3:]

            try:
                pkt = VS2Header(msg_bytes)
            except:
                pkt = Raw(msg_bytes)
            self._pkt = pkt
            logger.debug(pkt.show(dump=True))
            self._message_event.set()
        else:
            logger.error("Unknown byte: %02x" % (self._buf[0]))
            self._buf = self._buf[1:]

    async def send(self, data, timeout=3):
        self._transport.write(data)
        await asyncio.wait_for(self._ack_event.wait(), timeout)

    async def send_recv(self, data, timeout=3):
        await self.send(data, timeout)
        await asyncio.wait_for(self._message_event.wait(), timeout)
        return self._pkt

    def disconnect_viessmann(self):
        self._transport.write(self._END_COMMUNICATION)

    async def connect_viessmann(self, timeout=10):
        logger.debug("viessmann disconnect")
        self.disconnect_viessmann()
        self._connecting = True
        logger.debug("viessmann wait for periodic event")
        await asyncio.wait_for(self._periodic_event.wait(), timeout)
        logger.debug("viessmann send ping")
        await self.send(self._PING)
        logger.debug("viessmann connected")

    def connection_lost(self, exc: Exception):
        logger.debug('port closed')
        if self._running and not self._lock.locked():
            asyncio.ensure_future(self._reconnect(), loop=self._loop)

    async def _create_connection(self):
        if self._url.scheme == 'socket':
            kwargs = {
                'host': self._url.hostname,
                'port': self._url.port,
            }
            coro = self._loop.create_connection(lambda: self, **kwargs)
        else:
            kwargs = {
                'url': self._url.geturl(),
                'baudrate': self._BAUD_RATE,
                'parity': serial.PARITY_EVEN,
                'stopbits': serial.STOPBITS_TWO
            }
            coro = create_serial_connection(self._loop, lambda: self, **kwargs)
        return await coro

    async def _reconnect(self, delay: int = 10):
        async with self._lock:
            await self._disconnect()
            await asyncio.sleep(delay, loop=self._loop)
            try:
                async with timeout(5, loop=self._loop):
                    self._transport, _ = await self._create_connection()
            except (BrokenPipeError, ConnectionRefusedError,
                    SerialException, asyncio.TimeoutError) as exc:
                logger.warning(exc)
                asyncio.ensure_future(self._reconnect(), loop=self._loop)
            else:
                logger.debug("Serial port opened. Doing Viessman conect")
                await self.connect_viessmann()
                logger.info('Connected to %s', self._url.geturl())

    async def connect(self, loop=None):
        if self._running:
            return

        if not loop:
            loop = asyncio.get_event_loop()

        self._loop = loop
        self._lock = asyncio.Lock(loop=loop)
        self._running = True
        await self._reconnect(delay=0)

    async def _disconnect(self):
        if self._transport:
            self._transport.abort()
            self._transport = None
