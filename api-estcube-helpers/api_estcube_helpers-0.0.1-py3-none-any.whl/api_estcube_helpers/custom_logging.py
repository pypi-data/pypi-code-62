#DESCRIPTION: Logging functions.

#TODO: Implement proper error handling

import asyncio
import json
import logging
import threading
from datetime import datetime
from queue import Queue

notifier = None
logger   = None

class CustomLogging(logging.Logger):
    def __init__(self, name, level = logging.NOTSET):
        self._count = 0
        self._countLock = threading.Lock()
        return super(Logging, self).__init__(name, level)

    def set_server(self, server):
        self.server = server

    def setLevel(self, lvl):
        return super(Logging, self).setLevel(lvl)

    #def debug(self, msg, *args, **kwargs):
        #msg_object = {
          # "type": "debug",
          # "msg": msg,
          # "time": "{}".format(datetime.now().isoformat())
       # }
        #send_log_to_server(json.dumps(msg_object))
       # return super(Logging, self).debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        msg_object = {
            "type": "info",
            "msg": msg,
            "time": "{}".format(datetime.now().isoformat())
        }
        asyncio.create_task(self.send_log_to_server(json.dumps(msg_object)))
        return super(Logging, self).info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        msg_object = {
            "type": "warning",
            "msg": msg,
            "time": "{}".format(datetime.now().isoformat())
        }
        asyncio.create_task(self.send_log_to_server(json.dumps(msg_object)))
        return super(Logging, self).warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        msg_object = {
            "type": "error",
            "msg": msg,
            "time": "{}".format(datetime.now().isoformat())
        }
        asyncio.create_task(self.send_log_to_server(json.dumps(msg_object)))
        return super(Logging, self).error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        msg_object = {
            "type": "critical",
            "msg": msg,
            "time": "{}".format(datetime.now().isoformat())
        }
        asyncio.create_task(self.send_log_to_server(json.dumps(msg_object)))
        return super(Logging, self).critical(msg, *args, **kwargs)

    def log(self, lvl, msg, *args, **kwargs):
        msg_object = {
            "type": lvl,
            "msg": msg,
            "time": "{}".format(datetime.now().isoformat())
        }
        asyncio.create_task(self.send_log_to_server(json.dumps(msg_object)))
        return super(Logging, self).log(lvl, msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        msg_object = {
            "type": "exception",
            "msg": msg,
            "time": "{}".format(datetime.now().isoformat())
        }
        asyncio.create_task(self.send_log_to_server(json.dumps(msg_object)))
        return super(Logging, self).exception(msg, *args, **kwargs)

    async def send_log_to_server(self, log):
        await self.server.broadcast_message(log)
