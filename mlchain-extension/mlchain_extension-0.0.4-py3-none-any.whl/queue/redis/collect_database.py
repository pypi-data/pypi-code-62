import redis
from pymongo.mongo_client import MongoClient
from mlchain import logger
from mlchain_extension.queue.redis.base import MLCHAIN_DATABASE_QUEUE
import time
from mlchain.base import MsgpackSerializer
import os


class CollectDatabase:
    def __init__(self, redis_host=None, redis_port=None, redis_db=None, redis_pass=None, mongo_connection=None):
        self.host = redis_host or os.getenv('REDIS_HOST', 'localhost')
        self.port = redis_port or os.getenv('REDIS_PORT', 6379)
        self.db = redis_db or int(os.getenv('REDIS_DB', 0))
        self.password = redis_pass or os.getenv('REDIS_PASSWORD', '')
        self.redis_client = redis.Redis(host=self.host, port=self.port, db=self.db, password=self.password)
        self.mongo_client = MongoClient(mongo_connection or os.getenv("MONGO_CONNECTION"))
        self.serializer = MsgpackSerializer()
        self.collection = self.mongo_client['mlchain']['task_queue']

    def callback(self, msg):
        msg_type = msg.get('type', None)
        if msg_type == 'task':
            task_id = msg['context_id']
            required = msg['required']
            if isinstance(required, str):
                required = [required]
            self.collection.insert({'_id': task_id, 'task_id': task_id, 'sub_tasks': required, 'status': 'PENDING','name':msg['post_process'],'type':'children'})
        elif msg_type == 'call':
            task_id = msg['key']
            self.collection.insert(
                {'_id': task_id, 'task_id': task_id, 'status': 'PROCESSING', 'type': 'root', 'sub_tasks': [],'name':msg['name'],'function':msg['function_name']})
        elif msg_type == 'run':
            task_id = msg['key']
            self.collection.update({'_id': task_id}, {'$set': {'status': 'PROCESSING'}})
        elif msg_type == 'depend':
            task_id = msg['context_id']
            depend_task = msg['depend_task']
            self.collection.update({'_id': task_id}, {"$push": {'sub_tasks': depend_task}})
        elif msg_type == 'retry':
            task_id = msg['key']
            self.collection.update({'_id': task_id}, {'$set': {'status': 'RETRY'}, '$push': {'error': msg['error']}})
        else:
            if 'context_id' in msg:
                task_id = msg['context_id']
            else:
                task_id = msg['key']
            if 'error' in msg:
                self.collection.update({'_id': task_id}, {'$set': {'status': 'FAILURE'}})
            else:
                self.collection.update({'_id': task_id}, {'$set': {'status': 'SUCCESS'}})

    def run(self):
        logger.info("Start collect")
        while True:
            try:
                while True:
                    msg = self.redis_client.rpop(MLCHAIN_DATABASE_QUEUE)
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
    CollectDatabase().run()
