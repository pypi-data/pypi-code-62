"""Main module."""
#!/usr/bin/env python
# coding: utf-8
import os
import requests
import logging, logging.handlers
import datetime
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

# Logging
formatter = logging.Formatter("%(asctime)s | %(name)s |  %(levelname)s: %(message)s")
logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.addHandler(console_handler)
logger.setLevel(logging.INFO)


def run_watcher(auth, repdirs):
    def upload_sc2repstats(path):
        headers = {"Authorization": auth}
        url = "http://api.sc2replaystats.com/replay"
        data = {"upload_method": "ext"}
        logger.info(f"Uploading game at {path} to sc2replaystats")
        with open(path, "rb") as f:
            r = requests.post(url, files={"replay_file": f}, data=data, headers=headers)
            if r.status_code == 200:
                logger.info("Successfully uploaded replay.")
            else:
                logger.error(f"Failed to upload replay. Response text is: {r.text}")
        return r

    class ReplayHandler(PatternMatchingEventHandler):
        def on_created(self, event):
            path = event.src_path
            logger.info(f"Found new replay at {path}")

            time.sleep(3)
            try:
                upload_sc2repstats(path)
            except:
                logger.exception(f"Failed to upload {path}. Skipping.")

    logger.info("Program started.")
    logger.info(f"Watching paths: {repdirs}")

    observer = Observer()
    event_handler = ReplayHandler(patterns=["*.SC2Replay"])
    for repdir in repdirs:
        observer.schedule(event_handler, repdir, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    return 0
