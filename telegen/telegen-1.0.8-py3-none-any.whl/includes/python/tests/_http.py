from asyncio import Protocol, Queue as AsyncQueue


class TCP(Protocol):
    __slots__ = ["transport", "future"]

    def connection_made(self, transport):
        self.transport = transport

    def connection_lost(self, exc):
        if exc:
            self.future.set_exception(exc)

    def data_received(self, data):
        body = data.split(b"\r\n\r\n", 1)[1]
        self.future.set_result(body)

    def eof_received(self):
        return False


class HttpConnectionPool:
    def __init__(self, host, *, loop, size):
        self.host = host
        self.loop = loop

        self.queue = AsyncQueue()
        self.tasks = [loop.create_task(self.open()) for _ in range(size)]

    async def open(self):
        transport = None

        queue = self.queue
        loop = self.loop
        host = self.host

        while True:
            (future, req) = await queue.get()

            if transport is None:
                (transport, protocol) = await loop.create_connection(lambda: TCP(), host, 443, ssl=True)

            protocol.future = future
            transport.write(req)
            await future

            if queue.empty():
                transport.close()
                transport = None

    def stop(self):
        for task in self.tasks:
            task.cancel()

    def request(self, path, method="GET", headers=None, body=None):
        # fmt: off
        req = (
            f"{method} /{path} HTTP/1.1\r\n"
            f"host: {self.host}\r\n"
        )
        # fmt: on

        if headers:
            req += "".join(f"{k}: {v}\r\n" for k, v in headers.items())

        req += "\r\n"
        req = req.encode()

        if body:
            req += body

        future = self.loop.create_future()
        self.queue.put_nowait((future, req))
        return future
