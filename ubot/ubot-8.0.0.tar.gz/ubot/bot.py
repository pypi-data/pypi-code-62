from abc import abstractmethod
from asyncio import get_event_loop, PriorityQueue as AsyncPriorityQueue, Protocol, Queue as AsyncQueue, QueueEmpty
from urllib.parse import urlencode


class ConnectionClosedException(Exception):
    pass


class TelegramHttpProtocol(Protocol):
    __slots__ = ["transport", "future"]

    def connection_made(self, transport):
        self.transport = transport

    def connection_lost(self, exc):
        if exc:
            self.future.set_exception(exc)

    def data_received(self, data):
        # we don't really need to parse anything
        body = data.split(b"\r\n\r\n", 1)[1]
        self.future.set_result(body)

    def eof_received(self):
        return False


class Bot:
    __slots__ = [
        "__token",
        "__max_connections",
        "__base_path",
        "__triggers",
        "__update_queue",
        "__connection_tasks",
        "__request_queue",
        "__is_running_task",
        "__is_stopped_future",
    ]
    update_types = (
        ("message", "message"),
        ("edited_message", "message"),
        ("channel_post", "message"),
        ("edited_channel_post", "message"),
        ("inline_query", "inline_query"),
        ("chosen_inline_result", "chosen_inline_result"),
        ("callback_query", "callback_query"),
        ("shipping_query", "shipping_query"),
        ("pre_checkout_query", "pre_checkout_query"),
    )

    def __init__(self, token, *, max_connections=5):
        """
        The Class(TM).

        :param token: The token given by BotFather
        :param max_connections: Max simultaneous open connections to Telegram's servers
        """

        self.__token = token
        self.__max_connections = max_connections

        self.__base_path = f"bot{token}/"
        self.__connection_tasks = []
        self.__request_queue = AsyncQueue()
        self.__triggers = []
        self.__update_queue = AsyncPriorityQueue()

    @abstractmethod
    async def before_handle(self, update: dict):
        """
        Executes some code once before all the triggers are checked and eventually executed. A falsy return value
        disables the execution of any trigger.

        :param update: A dict obtained by json decoding a Telegram update
        :return: A falsy value to disable the execution of the triggers, a truthy one otherwise
        """
        pass

    @abstractmethod
    async def after_handle(self, update: dict):
        """
        Executes some code once after all the triggers are checked and eventually executed (unless a trigger stops the
        loop by returning a truthy value).

        :param update: A dict obtained by json decoding a Telegram update
        """
        pass

    @staticmethod
    def get_type_and_flavor(update: dict):
        """
        Finds the type and flavor of the given update ("type" is the json field that contains an API object of type
        "flavor")

        :param update: A dict obtained by json decoding a Telegram update
        """

        for _type, flavor in Bot.update_types:
            if _type in update:
                update["_type"] = _type
                update["_flavor"] = flavor
                return
        else:
            update["_type"] = None
            update["_flavor"] = None

    async def api_request(self, request: tuple) -> bytes:
        """
        Makes a Telegram request with the params given in the BotRequest

        :param request: A tuple (method, endpoint, headers, params, body)
        :return: The response from the server (plaintext json)
        """

        method, endpoint, headers, params, body = request

        path = f"{self.__base_path}{endpoint}?{urlencode(params)}" if params else f"{self.__base_path}{endpoint}"

        # fmt: off
        req = (
            f"{method} /{path} HTTP/1.1\r\n"
            f"host: api.telegram.org\r\n"
        )
        # fmt: on

        if headers:
            req += "".join(f"{k}: {v}\r\n" for k, v in headers.items())

        req = req.encode()
        req += b"\r\n"

        if body:
            req += body

        loop = get_event_loop()
        future = loop.create_future()
        self.__request_queue.put_nowait((req, future))

        return await future

    def start(self, *, loop=None):
        """
        Open a pool of connections and start the bot loop, this function wraps start_async and provides the user a future that is completed when the bot is stopped.
        Alternatively, you can run start_async directly, but the Bot.stop() method won't work.

        :param loop: The event loop to start the bot in (default: asyncio.get_event_loop())
        """

        loop = loop or get_event_loop()

        self.__is_running_task = loop.create_task(self.start_async())

        # this future will be resolved once the bot is stopped
        is_stopped_future = loop.create_future()
        self.__is_stopped_future = is_stopped_future

        return is_stopped_future

    def stop(self):
        """Stop the bot loop, close all the connections and return exceptions on pending requests"""

        self.__is_running_task.cancel()

        for task in self.__connection_tasks:
            # TODO: should close open connections, how?
            task.cancel()
        self.__connection_tasks.clear()

        while True:
            try:
                _, future = self.__request_queue.get_nowait()
                future.set_exception(ConnectionClosedException)
            except QueueEmpty:
                break

        self.__is_stopped_future.set_result(True)

    def push_update(self, update: dict):
        """
        Pushes an update (already json decoded) into the queue.

        :param update: A dict obtained by json decoding a Telegram update
        """

        self.__update_queue.put_nowait((update["update_id"], update))

    def trigger(self, trigger):
        """
        Inserts the decorated callable it into the bot trigger list

        :param trigger: A callable that returns a truthy value if no trigger should be executed afterwards, falsy
            otherwise; it must take as parameters the json decoded update (a dict) and the Bot instance.
        :return trigger: The decorated callable
        """

        self.__triggers.append(trigger)
        return trigger

    async def start_async(self):
        """Opens N connection tasks and starts the bot loop"""

        # open the connection tasks
        loop = get_event_loop()

        for _ in range(self.__max_connections):
            self.__connection_tasks.append(loop.create_task(self.__open_connection()))

        # in order to avoid the "if self.method" evaluation for each update we define 4 versions of __handle update:
        # - one that only does the loop (no method implemented)
        # - one that calls before_update
        # - one that calls after_update
        # - one that calls both before_update and after_update
        # and based on which function is defined we start a different loop
        # N.B.: since the loop is started only once this version has no overhead once it's running, but the code is
        # significantly uglier
        # N.B: in this way we can also define them as abstractmethods and treat them as proper methods instead that
        # class variables

        # cache to avoid lookups
        triggers = self.__triggers

        update_queue = self.__update_queue

        before_handle = self.before_handle
        after_handle = self.after_handle

        is_before_handle_abstract = getattr(before_handle, "__isabstractmethod__", False)
        is_after_handle_abstract = getattr(after_handle, "__isabstractmethod__", False)

        if is_before_handle_abstract:
            if is_after_handle_abstract:
                # both methods are abstract --> only loop
                while True:
                    _, update = await update_queue.get()

                    for trigger in triggers:
                        if await trigger(self, update):
                            break

            else:
                # after is not abstract --> call after only
                while True:
                    _, update = await update_queue.get()

                    for trigger in triggers:
                        if await trigger(self, update):
                            break
                    await after_handle(update)

        elif is_after_handle_abstract:
            # before is not abstract --> call before only
            while True:
                _, update = await update_queue.get()

                if not await before_handle(update):
                    continue
                for trigger in triggers:
                    if await trigger(self, update):
                        break

        else:
            # both are not abstract --> call both before and after
            while True:
                _, update = await update_queue.get()

                if not await before_handle(update):
                    continue
                for trigger in triggers:
                    if await trigger(self, update):
                        break
                await after_handle(update)

    async def __open_connection(self):
        loop = get_event_loop()
        transport = None
        protocol = None

        request_queue = self.__request_queue

        while True:
            # wait for a request
            (request, future) = await request_queue.get()

            # open a connection if it's not open already
            if transport is None:
                (transport, protocol) = await loop.create_connection(
                    TelegramHttpProtocol, "api.telegram.org", 443, ssl=True
                )

            # write to the transport and await on the future
            protocol.future = future
            transport.write(request)
            await future

            # if there aren't requests in the queue close the connection
            if request_queue.empty():
                transport.close()
                transport = None
