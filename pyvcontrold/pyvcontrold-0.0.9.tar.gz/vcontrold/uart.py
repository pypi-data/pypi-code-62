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
        self._connected = False
        self._buf = b''
        self._lock = None
        self._viessmann_lock = None
        self._ack_event = asyncio.Event()
        self._periodic_event = asyncio.Event()
        self._result_future = None
        self.sent_pkt = None

    def data_received(self, data: bytes):
        self._transport.pause_reading()
        self._buf += data
        while len(self._buf) > 0:
            if self._buf[0] == self._ACK:
                self._buf = self._buf[1:]
                self._ack_event.set()
            elif self._buf[0] == self._PERIODIC_WORD:
                self._buf = self._buf[1:]
                if self._running:
                    if not self._viessmann_lock.locked():
                        logger.debug("Viessmann disconnected")
                        self._connected = False
                    else:
                        self._periodic_event.set()
            elif self._buf[0] == self._START_BYTE:
                if len(self._buf) < 3:
                    break

                length = self._buf[1]
                if len(self._buf) < length+3:
                    break

                msg_bytes, self._buf = self._buf[:length+3], self._buf[length+3:]

                try:
                    pkt = VS2Header(msg_bytes)
                except:
                    pkt = Raw(msg_bytes)

                if (not self._result_future) or \
                   self._result_future.done() or \
                   self._result_future.cancelled():
                    continue

                if pkt.answers(self._sent_pkt):
                    self._result_future.set_result(pkt)
                else:
                    logger.debug("packet is not answering")
                    self._result_future.cancel()
            else:
                logger.error("Unknown byte: %02x" % (self._buf[0]))
                self._buf = self._buf[1:]

        self._transport.resume_reading()

    async def _send_ack(self, data, timeout=3):
        self._transport.write(data)
        await asyncio.wait_for(self._ack_event.wait(), timeout)
        self._ack_event.clear()

    async def send_recv(self, pkt, timeout=3):
        if not self._connected:
            logger.debug("Reconnecting...")
            await self._reconnect_viessmann()
        self._sent_pkt = pkt
        self._result_future = self._loop.create_future()
        await self._send_ack(bytes(pkt), timeout)
        logger.debug("Request sent successfuly, waiting response...")
        answer = await asyncio.wait_for(self._result_future, timeout)
        logger.debug("Response received:")
        logger.debug(answer.show(dump=True))
        return answer

    async def _reconnect_viessmann(self):
        self._periodic_event.clear()
        async with self._viessmann_lock:
            self._transport.write(self._END_COMMUNICATION)
            await asyncio.wait_for(self._periodic_event.wait(), 4)
            await self._send_ack(self._PING, timeout=2)
            self._connected = True
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
                logger.info('Connected to %s', self._url.geturl())

    async def connect(self, loop):
        if self._running:
            return

        self._loop = loop
        self._lock = asyncio.Lock(loop=loop)
        self._viessmann_lock = asyncio.Lock(loop=loop)
        self._running = True
        await self._reconnect(delay=0)

    async def _disconnect(self):
        if self._transport:
            self._transport.abort()
            self._transport = None
