from tenacity import retry, wait_fixed, stop_after_attempt
from google.cloud import storage
import os
import requests
import sys
import time
import logging
import datetime

@retry(wait=wait_fixed(2), stop=stop_after_attempt(3))
def cp_batch(
    STORAGE_CLIENT,
    SRC_BUCKET,
    DEST_BLOB,
    DEST_BUCKET,
    PARENT_FOLDER,
    depth
):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    filehandler = logging.FileHandler('move.log')
    filehandler.setLevel(logging.INFO)

    if (logger.hasHandlers()):
        logger.handlers.clear()

    logger.addHandler(filehandler)
    logger.info('START Timestamp: {}'.format(datetime.datetime.now()))

    blobs = STORAGE_CLIENT.list_blobs(SRC_BUCKET)
    for blob in blobs:
        try:
            folders = blob.name.split('/')
            if PARENT_FOLDER in folders[depth]:
                cp_blob(
                    STORAGE_CLIENT,
                    blob.name,
                    DEST_BLOB + '/' + blob.name,
                    SRC_BUCKET,
                    DEST_BUCKET
                    )
        except Exception as e:
            print('Error: {}'.format(e))
            logger.info('Error: {}'.format(e))
            
@retry(wait=wait_fixed(2), stop=stop_after_attempt(3))
def cp_blob(
    STORAGE_CLIENT,
    blob_name,
    new_blob_name,
    bucket_name,
    new_bucket_name
    ):
    """
    Function for moving files between directories or buckets. it will use GCP's copy
    function then delete the blob from the old location.

    inputs
    -----
    bucket_name: name of bucket
    blob_name: str, name of file
    ex. 'data/some_location/file_name'
    new_bucket_name: name of bucket (can be same as original if we're just moving around directories)
    new_blob_name: str, name of file in new directory in target bucket
    ex. 'data/destination/file_name'
    """
    source_bucket = STORAGE_CLIENT.get_bucket(bucket_name)
    source_blob = source_bucket.get_blob(blob_name)
    destination_bucket = STORAGE_CLIENT.get_bucket(new_bucket_name)
    
    time.sleep(0.05)

    # get size of blob
    blob_size = source_blob.size

    # rewrite of blob greater than 15mb
    if (blob_size > 15000000):
        url = """https://storage.googleapis.com/storage/v1/b/
                {}/o/{}/rewriteTo/b/
                {}/o/{}""".format(
                    source_bucket, 
                    source_blob,
                    destination_bucket,
                    new_blob_name)
        try:
            requests.post(url)
            logger.info('rewritten {} to {}\n'.format(source_blob.name, new_blob_name))
            print('rewritten {} to {}\n'.format(source_blob.name, new_blob_name))
        except Exception as e:
            logger.info('Error: {}'.format(e))
            print('Error: {}'.format(e))
    else:
        #copy to new destination
        new_blob = source_bucket.copy_blob(source_blob, destination_bucket, new_blob_name)
        logger.info('copied {} to {}\n'.format(source_blob.name, new_blob_name))
        print('copied {} to {}\n'.format(source_blob.name, new_blob_name))            