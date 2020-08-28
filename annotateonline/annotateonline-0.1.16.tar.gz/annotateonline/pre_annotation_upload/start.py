import json
import boto3
import traceback
import threading
from queue import Queue
from threading import Thread
import os
from .coco_convert import get_jsons_dict

class AppWorkerCoco(Thread):

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            image_name,image_data,args,logger = self.queue.get()
            try:
                logger.info('runing {}'.format(image_name))
                upload_coco_annotation(image_name,image_data,args,logger)
            finally:
                self.queue.task_done()

class AppWorkerAo(Thread):

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            file_path,args,logger = self.queue.get()
            try:
                logger.info('runing {}'.format(file_path))
                upload_ao_annotations(file_path,args,logger)
            finally:
                self.queue.task_done()


def upload_coco_annotation(image_name,image_data,args,logger):
    try:
        logger.info('start---'+image_name+'----')
        destination = args.destination
        bucket = args.bucket
        session = boto3.Session(aws_access_key_id=args.aws_access_key_id,aws_secret_access_key=args.aws_secret_access_key,aws_session_token=args.aws_session_token)
        s3 = session.resource('s3')
        my_bucket = s3.Bucket(args.bucket)
        put_data = my_bucket.put_object(Body=json.dumps(image_data), Bucket=bucket, Key=destination + '/' + image_name + '___objects.json', ContentType="application/json")
        logger.info('done---'+image_name+'----')
    except Exception as e:
        logger.error(traceback.format_exc())
    
def upload_ao_annotations(file_path,args,logger):
    try:
        logger.info('start---'+file_path+'----')
        file_name = file_path.split('/')[-1]
        destination = args.destination
        bucket = args.bucket
        session = boto3.Session(aws_access_key_id=args.aws_access_key_id,aws_secret_access_key=args.aws_secret_access_key,aws_session_token=args.aws_session_token)
        s3 = session.resource('s3')
        my_bucket = s3.Bucket(args.bucket)
        put_data = my_bucket.upload_file(file_path,destination + '/' + file_name )
        logger.info('done---'+file_name+'----')
    except Exception as e:
        logger.error(traceback.format_exc())

def start(args,logger):
    queue = Queue()    
    if(args.ao_jsons):
        for x in range(8):
            worker = AppWorkerAo(queue)
            worker.daemon = True
            worker.start()
        pwd = args.ao_jsons
        files = os.listdir(pwd)
        if pwd[-1] != '/':
            pwd += '/'
        for f in files:
            if not '___objects.json' in f:
                continue
            file_path = pwd + f
            logger.info('Queueing {}'.format(file_path))
            queue.put((file_path,args,logger))            
        queue.join()

    if(args.coco_json):
        for x in range(8):
            worker = AppWorkerCoco(queue)
            worker.daemon = True
            worker.start()
        coco_json_path = args.coco_json
        ao_jsons = get_jsons_dict(coco_json_path)
        for image_name in ao_jsons:
            logger.info('Queueing {}'.format(image_name))
            queue.put((image_name,ao_jsons[image_name],args,logger))
        queue.join()

