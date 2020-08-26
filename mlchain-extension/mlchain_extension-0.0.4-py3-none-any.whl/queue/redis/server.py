from mlchain_extension.queue.base import QueueModel
from .base import RedisBase, MLCHAIN_EVENT_QUEUE, redis_client, MLCHAIN_DATABASE_QUEUE
from mlchain_extension.queue import MlchainSameResultResponse
import time
from bson.objectid import ObjectId
from threading import Thread
from mlchain import mlchain_context, logger
import traceback


class RedisQueue(QueueModel, RedisBase):
    def __init__(self, model, host=None, port=None, db=None, password=None, deny_all_function=False, blacklist=[],
                 whitelist=[], version='0.0', name='MLChain', config=None):
        QueueModel.__init__(self, model, deny_all_function, blacklist, whitelist)

        if config is None:
            config = []
            model = self.model
            for attr_name in dir(model):
                attr = getattr(model, attr_name)
                queue_name = getattr(attr, '__queue__', None)
                if isinstance(queue_name, str):
                    config.append({
                        'function_name': attr_name,
                        'input': queue_name
                    })
        else:
            model = self.model
            config = list(config)
            for idx, c in enumerate(config):
                if isinstance(c, dict):
                    func = getattr(model, c['function_name'])
                    if 'input' in c:
                        setattr(func.__func__, '__queue__', c['input'])
                    else:
                        setattr(func.__func__, '__queue__', func.__func__.__qualname__)
                else:
                    func = getattr(model, c)
                    if hasattr(func, '__func__'):
                        queue_name = func.__func__.__qualname__
                        setattr(func.__func__, '__queue__', queue_name)
                    else:
                        queue_name = func.__qualname__
                        setattr(func, '__queue__', queue_name)
                    config[idx] = {'function_name': c, 'input': queue_name}
        RedisBase.__init__(self, host=host, port=port, db=db, password=password, version=version, name=name,
                           config=config)
        self.client.set('mlchain_queue_{0}:{1}'.format(self.name, self.version), self.serializer.encode(self.config))
        self.running = None

    def callback(self, config, msg):
        key = msg.get("key", None)

        if key is None:
            key = str(ObjectId()).encode()

        args, kwargs = self.get_params(msg["value"])
        context = msg.get('context', {})
        if context.get('context_id', None) is None:
            context['context_id'] = key
        if 'output_topic' in context:
            output_topic = context.pop('output_topic')
        else:
            output_topic = None
        mlchain_context.set(context)
        try:
            output = self.call_function(config['function_name'], key, *args, **kwargs)
            if isinstance(output, MlchainSameResultResponse):
                self.client.lpush(MLCHAIN_EVENT_QUEUE, self.serializer.encode({
                    'type': 'depend',
                    'context_id': key,
                    'depend_task': output.task_id,
                    'function_name': config['function_name']
                }))
                return
            self.client.set(key, self.serializer.encode(output))
            self.client.lpush(MLCHAIN_EVENT_QUEUE, self.serializer.encode({
                "key": key,
                "context": mlchain_context.copy(),
                'function_name': config['function_name']
            }))
            if 'output' in config:
                self.client.lpush(config['output'], self.serializer.encode({
                    "key": key,
                    "context": mlchain_context.copy()
                }))
            if output_topic is not None:
                self.client.lpush(output_topic, self.serializer.encode({
                    "key": key,
                    "context": mlchain_context.copy()
                }))
        except Exception as e:
            error = ''.join(traceback.extract_tb(e.__traceback__).format()).strip()
            logger.error(error)
            if 'RETRY' not in context:
                context['RETRY'] = 0
            if context['RETRY'] < config['retry']:
                context['RETRY'] += 1
                msg['context'] = context
                msg['type'] = 'retry'
                msg['error'] = error
                self.client.lpush(config['input'], self.serializer.encode(msg))
            else:
                output = {"error": error}
                self.client.set(key, self.serializer.encode(output))
                self.client.lpush(MLCHAIN_EVENT_QUEUE, self.serializer.encode({
                    "key": key,
                    "context": mlchain_context.copy(),
                    'function_name': config['function_name'],
                    'error': error
                }))
                if 'output' in config:
                    self.client.lpush(config['output'], self.serializer.encode({
                        "key": key,
                        "context": mlchain_context.copy(),
                        'error': error
                    }))
                if output_topic is not None:
                    self.client.lpush(output_topic, self.serializer.encode({
                        "key": key,
                        "context": mlchain_context.copy(),
                        'error': error
                    }))
            return

    def call_async(self, function_name, key=None, *args, **kwargs):
        context = mlchain_context.get()
        return self.publish(function_name=function_name, key=key, args=args, kwargs=kwargs, context=context)

    def get_params(self, value):
        if isinstance(value, dict) and 'args' in value and 'kwargs' in value:
            return value.get('args', []), value.get('kwargs', {})
        else:
            return [value], {}

    def run(self, threading=False):
        self.running = True
        threads = []
        for config in self.config:
            thread = Thread(target=self.background, args=[config])
            thread.start()
            threads.append(thread)
        if not threading:
            for thread in threads:
                thread.join()

    def background(self, config):
        if 'retry' not in config:
            config['retry'] = 0
        redis_client.set(self.client)
        while self.running:
            try:
                while self.running:
                    msg = self.client.rpoplpush(config['input'], MLCHAIN_DATABASE_QUEUE)
                    if msg is None:
                        time.sleep(0.1)
                        continue
                    msg = self.serializer.decode(msg)
                    self.callback(config, msg)
            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.error(str(e))
                raise e
                continue
