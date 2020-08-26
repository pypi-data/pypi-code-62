# -*- coding: utf-8 -*-
import logging

import threading
import zmq
from zmq.utils.monitor import recv_monitor_message

logger = logging.getLogger(__name__)

class StreamOutput(object):
    """
    Output instance. Connects to remote socket and relies the zmq frames.

    Uses zmq-socket-monitor to see if we are connected to the subscriber.
    """
    def __init__(self, zmq_ctx, output):
        self.zmq_ctx = zmq_ctx
        self.output = output
        logger.debug('Connecting output to {}'.format(self.output))
        self.connection = self.zmq_ctx.socket(zmq.PUB)
        self._monitor_thread = threading.Thread(target=StreamOutput._monitor, args=(self,))
        self._monitor_thread.start()
        self.connection.connect(self.output)
        self.connected = True

        self._num_subscribers_lock = threading.Lock()
        self._num_subscribers = 0

    def _monitor(self):
        #return
        # TODO: fox zmq monitoring
        try:
            monitor = self.connection.get_monitor_socket()
            while monitor.poll():
                evt = recv_monitor_message(monitor)
                if evt['event'] == zmq.EVENT_CONNECTED:
                    self._num_subscribers_lock.acquire()
                    self._num_subscribers += 1
                    self._num_subscribers_lock.release()
                elif evt['event'] == zmq.EVENT_DISCONNECTED:
                    self._num_subscribers_lock.acquire()
                    self._num_subscribers -= 1
                    self._num_subscribers_lock.release()
                elif evt['event'] == zmq.EVENT_MONITOR_STOPPED:
                    break
            monitor.close()

        except zmq.ZMQError as e:
            # TODO: how to handle this case? what did went wrong?
            logger.error('Unable to initialize monitor - {}'.format(e))

    def is_connected(self):
        self._num_subscribers_lock.acquire()
        num_sub = self._num_subscribers
        self._num_subscribers_lock.release()
        return num_sub > 0

    def stop(self):
        logger.debug('Stopping output to {}'.format(self.output))
        try:
            self.connection.disable_monitor()
        except Exception as e:
            logger.warning('StreamOutput.disconnect exception - error while disabling monitor: {}'.format(e))
        # close zmq socket
        self.connection.close()
        self.connected = False

    def __str__(self):
        self._num_subscribers_lock.acquire()
        num_sub = self._num_subscribers
        self._num_subscribers_lock.release()
        return '<StreamOutput: {} {}>'.format(self.output, num_sub)

    def send(self, frame):
        """
        passing the zmq frame to the output's connection
        """
        self.connection.send(frame, zmq.NOBLOCK)
