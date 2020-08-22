#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#
# Hydra - The water monster of legend with multiple serpent heads on one body. This is the batch and worker system for downtime/background processing.
#         Main Thread is just a control. Hydra is the "batch" which checks what should run. HydraHeads are worker threads operating the hydra_queue.

# Python Imports
import datetime
import logging
import random
import signal
import sys
import threading
import time
import traceback

# Extern Imports
import tornado.options
from tornado.options import define, options

# Project Imports
import aegis.stdlib
import aegis.model


define('hydra_id', default=0, type=int)
define('hydra_sleep', default=1, type=int)


class HydraThread(threading.Thread):

    # quitting is at the class level to synchronize the threads in the process
    quitting = False
    filename = __file__


    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        self.logw = aegis.stdlib.logw
        self.start_t = time.time()
        self.processed_cnt = 0
        self.iter_cnt = 0
        self.last_id = 0


    def run(self):
        try:
            self.process()
        except Exception as ex:
            logging.exception(ex)
            # XXX TODO chat_hook debug_hook


    def finish(self):
        end_t = time.time()
        exec_t = end_t - self.start_t
        recs_s = max(float(self.processed_cnt), 1.0) / exec_t
        recs_h = max(float(self.processed_cnt), 1.0) / exec_t * 3600
        logging.info("%s ending.  Records: %d   Seconds: %4.3f   Records/sec: %4.3f   Records/hr: %4.3f   Iterations: %s  Last Id: %s", self.name, self.processed_cnt, exec_t, recs_s, recs_h, self.iter_cnt, self.last_id)


    def main_thread(self):
        # Handling signals only works in the main thread
        signal.signal(signal.SIGINT, self.signal_stop)
        signal.signal(signal.SIGTERM, self.signal_stop)
        signal.signal(signal.SIGUSR1, self.signal_debug)
        signal.signal(signal.SIGHUP, self.signal_reset)
        # Main thread is used only as a control thread... monitors quitting variable, and sleep gets interrupted by signal. And that's it!
        while threading.active_count() > 1:
            if HydraThread.quitting:
                logging.warning("aegis/hydra.py waiting %ss for threads to finish... %s active" % (options.hydra_sleep, threading.active_count()))
                threads = threading.enumerate()
                thr = random.choice(threads[1:])
                if thr != threading.current_thread():
                    thr.join(1.0)
            else:
                time.sleep(options.hydra_sleep)


    # Graceful shutdown with debug
    @staticmethod
    def signal_debug(sig, frame):
        """Interrupt running process, and provide a python prompt for interactive debugging."""
        id2name = dict([(th.ident, th.name) for th in threading.enumerate()])
        code = ["Received SIGUSR1 - Dumping Debug Output"]
        for threadId, stack in sys._current_frames().items():
            code.append("\n# Thread: %s(%d)" % (id2name.get(threadId,""), threadId))
            for filename, lineno, name, line in traceback.extract_stack(stack):
                code.append('File: "%s", line %d, in %s' % (filename, lineno, name))
                if line:
                    code.append("  %s" % (line.strip()))
        logging.warning("\n".join(code))


    @staticmethod
    def signal_stop(signal, frm):
        logging.warning('SIGINT or SIGTERM received (%s). Quitting now...', signal)
        HydraThread.quitting = True


    @staticmethod
    def signal_reset(signal, frm):
        logging.warning("SIGHUP received... clearing stale claims")
        aegis.model.HydraQueue.clear_claims()


class HydraHead(HydraThread):

    def __init__(self, hydra_head_id, *args, **kwargs):
        self.hydra_head_id = hydra_head_id
        self.thread_name = 'HydraHead-%02d' % self.hydra_head_id
        HydraThread.__init__(self, name=self.thread_name)


    def process(self):
        logging.info("Spawning %s", self.name)
        try:
            while(not HydraThread.quitting):
                if self.hydra_head_id == 0:
                    queue_items = aegis.model.HydraQueue.scan_work_priority()
                else:
                    queue_items = aegis.model.HydraQueue.scan_work()
                for hydra_queue in queue_items:
                    if HydraThread.quitting: break
                    try:
                        # Fetch rows from database queue and claim items before processing
                        if not hydra_queue: time.sleep(options.hydra_sleep); continue
                        claimed = hydra_queue.claim()
                        self.logw(claimed, "CLAIMED HYDRA QUEUE: %s" % hydra_queue['hydra_queue_id'])
                        if not claimed: continue
                        hydra_type = aegis.model.HydraType.get_id(hydra_queue['hydra_type_id'])
                        # Hydra Magic: Find the hydra_type specific function in a subclass of HydraHead
                        if not hydra_type:
                            logging.error("Missing hydra type for hydra_type_id: %s", hydra_type)
                            continue
                        if not hasattr(self, hydra_type['hydra_type_name']):
                            logging.error("Missing hydra function for hydra type: %s", hydra_type)
                            continue
                        self.iter_cnt += 1
                        work_fn = getattr(self, hydra_type['hydra_type_name'])
                        # Do the work
                        hydra_queue.incr_try_cnt()
                        hydra_queue.start()
                        result, work_cnt = work_fn(hydra_queue, hydra_type)
                        #self.logw(result, "RESULT")
                        #self.logw(work_cnt, "WORK CNT")
                        if result:
                            hydra_queue.complete()
                        else:
                            logging.error("hydra_queue_id %s failed, will retry every 15m", hydra_queue['hydra_queue_id'])
                            continue
                        # Worker accounting
                        logging.warning(self.log_line(hydra_type, work_cnt, " DONE"))
                        self.processed_cnt += work_cnt
                    except Exception as ex:
                        logging.error("Exception when working on hydra_queue_id: %s", hydra_queue['hydra_queue_id'])
                        logging.exception(ex)
                        hydra_queue.incr_error_cnt()
                        hydra_queue.unclaim()
                # Iterate!
                time.sleep(options.hydra_sleep)
        except Exception as ex:
            logging.exception(ex)
        finally:
            self.finish()


    def log_line(self, hydra_type, work_cnt=0, msg=''):
        return '%s %s %s %s' % (self.name, hydra_type['hydra_type_name'], ("%d" % work_cnt).rjust(8), msg)


class Hydra(HydraThread):

    def __init__(self):
        self.hydra_id = options.hydra_id
        self.thread_name = 'Hydra-%02d' % options.hydra_id
        HydraThread.__init__(self, name=self.thread_name)
        self.num_heads = 3
        self.hydra_head_cls = HydraHead


    def spawn_heads(self):
        for ndx in range(0, self.num_heads):
            time.sleep(1)
            head = self.hydra_head_cls(ndx)
            head.start()


    def process(self):
        logging.info("Spawning %s" % self.name)
        # When starting up, hydra_id 0 clears claims before spawning heads.
        if self.hydra_id == 0:
            logging.warning("%s clearing stale claims" % self.name)
            aegis.model.HydraQueue.clear_claims()
            # If the hydra_type_id for this queue item has next_run_sql then it should be a singleton across the hydras.
            # This means set hydra_type['status'] = 'running' and set it back to 'live' after completion.
            logging.warning("%s clearing running jobs over 45 minutes old" % self.name)
            aegis.model.HydraType.clear_running()
        try:
            self.spawn_heads()
            while(not HydraThread.quitting):
                self.iter_cnt += 1
                try:
                    # Batch Loop: scan hydra_type for runnable batches
                    for hydra_type in aegis.model.HydraType.scan():
                        if HydraThread.quitting: break
                        # Check if the task is runnable
                        runnable = aegis.model.HydraType.get_runnable(hydra_type['hydra_type_id'])
                        if runnable:
                            # Set up a hydra_queue row to represent the work and re-schedule the batch's next run
                            hydra_queue = {}
                            hydra_queue['hydra_type_id'] = hydra_type['hydra_type_id']
                            hydra_queue['priority_ndx'] = hydra_type['priority_ndx']
                            hydra_queue['work_dttm'] = aegis.database.Literal("NOW()")
                            hydra_queue_id = aegis.model.HydraQueue.insert_columns(**hydra_queue)
                            hydra_type.schedule_next()
                            _hydra_type = aegis.model.HydraType.get_id(hydra_type['hydra_type_id'])
                            logging.warning("%s queue up %s   Next Run: %s" % (self.name, _hydra_type['hydra_type_name'], _hydra_type['next_run_dttm']))
                            # Clean out queue then sleep depending on how much work there is to do
                            purged_completed = aegis.model.HydraQueue.purge_completed()
                            if purged_completed:
                                logging.warning("%s queue purge deleted %s hydra_queue" % (self.thread_name, purged_completed))
                            # Log if there are expired queue items in the past...
                            past_items = aegis.model.HydraQueue.past_items()
                            if past_items and len(past_items):
                                logging.error("HydraQueue has %s stuck items", len(past_items))
                                for past_item in past_items:
                                    logging.error("Stuck hydra_queue_id: %s", past_item['hydra_queue_id'])
                                    #logging.error("Unclaiming stuck hydra_queue_id: %s", past_item['hydra_queue_id'])
                                    #past_item.unclaim()

                except Exception as ex:
                    logging.exception("Batch had an inner loop failure.")
                    # Chat Hooks?
                # Iterate!
                #logging.warning("The great hydra sleeps...")
                time.sleep(options.hydra_sleep)
        except Exception as ex:
            logging.exception(ex)
            traceback.print_exc()
            # Alert and debug hooks


        finally:
            self.finish()


if __name__ == "__main__":
    tornado.options.parse_command_line()
    hydra = Hydra()
    hydra.start()
    hydra.main_thread()
    sys.exit(0)
