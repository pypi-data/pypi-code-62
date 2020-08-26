from mlchain_extension.queue.base import QueueModel
from mlchain.base.serializer import MsgpackSerializer
import kafka
import pymongo
import time
from bson.objectid import ObjectId
from threading import Thread
import gridfs
from mlchain import mlchain_context, logger
import os


class KafkaBase:
    def __init__(self, bootstrap_servers=None, mongo_connection=None, version='0.0', name='MLChain',
                 input_topic=None):
        self.bootstrap_servers = bootstrap_servers or os.getenv('KAFKA_BOOTSTRAP_SERVERS', '127.0.0.1:9092')
        self.mongo_connection = mongo_connection or os.getenv('MONGO_CONNECTION')
        self.dataset = pymongo.MongoClient(connect=self.mongo_connection)['mlchain_queue']
        self.collection = self.dataset['task']
        self.file_storage = gridfs.GridFS(self.dataset)
        prefix = []
        self.version = version
        self.name = name
        prefix.append(name)
        prefix.append(version)
        self.input_topic = input_topic or '.'.join(prefix + ['input'])
        logger.info('listen topic: {0}'.format(self.input_topic))
        self.serializer = MsgpackSerializer()
        self.producer = kafka.KafkaProducer(bootstrap_servers=self.bootstrap_servers, acks=1,
                                            value_serializer=self.serializer.encode)

    def result(self, key):
        output = self.collection.find_one({'_id': key})
        if output:
            status = output.get('status')
            if status == 'SUCCESS':
                output_id = output['output']
                out = self.file_storage.get(ObjectId(output_id)).read()
                out = self.serializer.decode(out)
            else:
                out = None
            return {'status': status, 'output': out, 'time': output.get('time', 0)}
        return {'status': None, 'output': None, 'time': 0}

    def publish(self, function_name, key, args, kwargs, context):
        if key is None:
            key = str(ObjectId())
        timestamp = int(time.time())
        timezone = time.timezone

        inputs = {
            'args': args,
            'kwargs': kwargs
        }
        inputs = self.serializer.encode(inputs)
        input_id = self.file_storage.put(inputs, metadata=context)
        input_id = str(input_id)
        self.collection.insert({'_id': key, 'status': 'PENDING',
                                'uid': key,
                                'timestamp': timestamp,
                                'timezone': timezone,
                                'input': input_id
                                })
        try:
            self.producer.send(self.input_topic, {
                'input': input_id,
                'uid': key,
                'context': context,
                'function_name': function_name
            })
            return key
        except Exception as e:
            logger.error(str(e))
            self.collection.update({'_id': key}, {'$set': {'status': 'FAILURE'}}, multi=True)
            return None


class KafkaQueue(QueueModel, KafkaBase):
    def __init__(self, model, bootstrap_servers=None, mongo_connection=None,
                 deny_all_function=False,
                 blacklist=[], whitelist=[], version='0.0', name='MLChain',
                 input_topic=None, output_topic=None, retry=1):
        QueueModel.__init__(self, model, deny_all_function, blacklist, whitelist)
        KafkaBase.__init__(self, bootstrap_servers, mongo_connection, version=version, name=name,
                           input_topic=input_topic)
        self.output_topic = output_topic
        logger.info('response topic: {0}'.format(self.output_topic))
        self.running = None
        self.retry = retry

    def callback(self, msg):
        function_name = msg['function_name']
        key = msg['uid']

        if key is None:
            key = str(ObjectId())

        data = self.file_storage.get(ObjectId(msg['input'])).read()
        data = self.serializer.decode(data)
        args, kwargs = self.get_params(data)
        context = msg.get('context', {})
        if context.get('context_id', None) is None:
            context['context_id'] = key
        mlchain_context.set(context)
        self.collection.update({'_id': key}, {"$set": {'status': 'PROCESSING', 'context': context,
                                                       'name': self.name, 'version': self.version,
                                                       'function': function_name}}, multi=True)
        try:
            start = time.time()
            output = self.call_function(function_name, key, *args, **kwargs)
            output_encoded = self.serializer.encode(output)
            output_id = self.file_storage.put(output_encoded, metadata=mlchain_context.copy())
            output_id = str(output_id)
            self.collection.update({'_id': key},
                                   {"$set": {'status': 'SUCCESS', 'output': output_id,
                                             'time': time.time() - start}}, multi=True)
            if isinstance(self.output_topic, str):
                self.producer.send(self.output_topic, output)
        except Exception as e:
            logger.error(str(e))
            self.collection.update({'_id': key}, {"$set": {'status': 'FAILURE'}}, multi=True)

            if 'RETRY' not in context:
                context['RETRY'] = 0
            if context['RETRY'] < self.retry:
                context['RETRY'] += 1
                msg['context'] = context
                key = str(ObjectId())
                timestamp = int(time.time())
                timezone = time.timezone
                msg['uid'] = key
                self.collection.insert({'_id': key, 'status': 'PENDING',
                                        'uid': key,
                                        'timestamp': timestamp,
                                        'timezone': timezone,
                                        'input': msg['input']
                                        })

                self.producer.send(self.input_topic, msg)
            return

    def call_async(self, function_name_, key_=None, *args, **kwargs):
        function_name, key = function_name_, key_
        context = mlchain_context.get()
        return self.publish(function_name=function_name, key=key, args=args, kwargs=kwargs, context=context)

    def get_params(self, value):
        return value.get('args', []), value.get('kwargs', {})

    def run(self, threading=False):
        self.running = True
        self.threat = None
        if not threading:
            self.background()
        else:
            if self.threat is None:
                self.threat = Thread(target=self.background)
                self.threat.start()
            elif not self.threat.is_alive():
                self.threat = Thread(target=self.background)
                self.threat.start()

    def background(self):
        while self.running:
            try:
                consumer = kafka.KafkaConsumer(bootstrap_servers=self.bootstrap_servers,
                                               auto_offset_reset='earliest', group_id='mlchain',
                                               enable_auto_commit=False,
                                               consumer_timeout_ms=10, value_deserializer=self.serializer.decode)
                consumer.subscribe([self.input_topic])
                logger.debug(str(consumer.subscription()))
                while self.running:
                    for message in consumer:
                        logger.debug((message.value))
                        try:
                            self.callback(message.value)
                            consumer.commit()
                        except Exception as e:
                            logger.error(str(e))
                            pass
                        if not self.running:
                            break

                consumer.close()
            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.error(str(e))
                continue
