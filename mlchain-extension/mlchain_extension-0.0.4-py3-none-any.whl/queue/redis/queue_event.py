from mlchain import logger
from mlchain.base import MsgpackSerializer
from redis import Redis
from mlchain_extension.queue.redis.base import MLCHAIN_EVENT_QUEUE,MLCHAIN_DATABASE_QUEUE
import time
import os


class Map:
    def __init__(self, client, serializer, prefix='data_queue'):
        self.client = client
        self.serializer = serializer
        self.prefix = prefix

    def __getitem__(self, item):
        data = self.client.get('{0}_{1}'.format(self.prefix, item))
        if data is None:
            return None
        return self.serializer.decode(data)

    def __setitem__(self, key, value):
        self.client.set('{0}_{1}'.format(self.prefix, key), self.serializer.encode(value))

    def get(self, key, default):
        data = self.client.get('{0}_{1}'.format(self.prefix, key))
        if data is None:
            return default
        return self.serializer.decode(data)


class QueueEventManager:
    def __init__(self, host=None, port=None, db=None, password=None):
        self.host = host or os.getenv('REDIS_HOST', 'localhost')
        self.port = port or os.getenv('REDIS_PORT', 6379)
        self.db = db or os.getenv('REDIS_DB', 0)
        self.password = password or os.getenv('REDIS_PASSWORD', '')
        self.serializer = MsgpackSerializer()
        self.client = Redis(host=self.host,
                            port=self.port,
                            password=self.password,
                            db=self.db)
        self.data = Map(self.client, self.serializer)

    def callback(self, msg):
        msg_type = msg.get('type', None)
        if msg_type == 'task':
            task_id = msg['context_id']
            required = msg['required']
            if isinstance(required, str):
                required = [required]
                self.data['{0}_arg'.format(task_id)] = 'one'
            else:
                self.data['{0}_arg'.format(task_id)] = 'many'
            for req in required:
                self.data['{0}_parent'.format(req)] = task_id
            self.data['{0}_children'.format(task_id)] = required
            if len(required)>0:
                count = len(required) - self.client.exists(*['{0}_done'.format(r) for r in required])
            else:
                count = 0
            self.data['{0}_count'.format(task_id)] = count
            self.data['{0}_post_process'.format(task_id)] = msg['post_process']
            self.data['{0}_type'.format(task_id)] = 'task'
            self.data['{0}_send_value'.format(task_id)] = msg['send_value']
            self.data['{0}_kwargs'.format(task_id)] = msg['kwargs']
            if count == 0:
                if self.data['{0}_send_value'.format(task_id)]:
                    args = [self.serializer.decode(self.client.get(id)) for id in required]
                    if self.data['{0}_arg'.format(task_id)] == 'many':
                        args = [args]
                else:
                    args = []
                self.client.rpush(msg['post_process'],
                                  self.serializer.encode(
                                      {
                                          'value': {
                                              'args': args,
                                              'kwargs': msg['kwargs']
                                          },
                                          'key': task_id,
                                          'type':'run'
                                      }))
        elif msg_type == 'depend':
            task_id = msg['context_id']
            depend_task = msg['depend_task']
            self.data['{0}_parent'.format(depend_task)] = task_id
            required = [depend_task]
            count = len(required) - self.client.exists(*['{0}_done'.format(r) for r in required])
            self.data['{0}_children'.format(task_id)] = required
            self.data['{0}_count'.format(task_id)] = count
            self.data['{0}_post_process'.format(task_id)] = None
            self.data['{0}_type'.format(task_id)] = 'depend'
            if count == 0:
                self.client.set(task_id, self.client.get(depend_task))
                self.client.rpush(MLCHAIN_EVENT_QUEUE, self.serializer.encode({
                    'context_id': task_id
                }))
        else:
            if 'context_id' in msg:
                task_id = msg['context_id']
            else:
                task_id = msg['key']
            self.client.setnx('{0}_done'.format(task_id), 'ok')
            parent_task = self.data.get('{0}_parent'.format(task_id), None)
            if parent_task is not None:
                type_parent = self.data['{0}_type'.format(parent_task)]
                if type_parent == 'depend':
                    self.client.set(parent_task, self.client.get(task_id))
                    self.data['{0}_count'.format(parent_task)] = 0
                    self.client.rpush(MLCHAIN_EVENT_QUEUE, self.serializer.encode({
                        'context_id': parent_task
                    }))
                elif type_parent == 'task':
                    count = self.data['{0}_count'.format(parent_task)]
                    count -= 1
                    self.data['{0}_count'.format(parent_task)] = count

                    if count == 0:
                        post_process = self.data['{0}_post_process'.format(parent_task)]
                        required = self.data['{0}_children'.format(parent_task)]
                        if self.data['{0}_send_value'.format(parent_task)]:
                            args = [self.serializer.decode(self.client.get(id)) for id in required]
                            if self.data['{0}_arg'.format(parent_task)] == 'many':
                                args = [args]
                        else:
                            args = []

                        self.client.rpush(post_process,
                                          self.serializer.encode(
                                              {
                                                  'value': {
                                                      'args': args,
                                                      'kwargs': self.data['{0}_kwargs'.format(parent_task)]
                                                  },
                                                  'key': parent_task,
                                                  'type':'run'
                                              }))

                else:
                    pass
            else:
                pass

    def run(self):
        logger.info("Start manager")
        while True:
            try:
                while True:
                    msg = self.client.rpoplpush(MLCHAIN_EVENT_QUEUE,MLCHAIN_DATABASE_QUEUE)
                    if msg is None:
                        time.sleep(0.05)
                        continue
                    msg = self.serializer.decode(msg)
                    logger.info(str(msg))
                    self.callback(msg)
            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.error(str(e))
                raise e


if __name__ == '__main__':
    QueueEventManager().run()
