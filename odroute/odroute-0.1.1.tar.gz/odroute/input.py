# -*- coding: utf-8 -*-
import time
import logging
import zmq

from zmq.eventloop.zmqstream import ZMQStream
from .frame import ZMQFrameDecoder

logger = logging.getLogger(__name__)

class StreamInput(object):
    """
    Input instance.
    """

    connected = False

    def __init__(self, zmq_ctx, port, delay_settings):
        """
        audio threshold is in range [-90..0] dB
        """
        self.zmq_ctx = zmq_ctx
        self.port = port
        self.delay_settings = delay_settings

        time_now = time.time()
        self._last_beat = time_now - float(self.delay_settings.nodata_failover_delay)
        self._last_audio_ok = time_now - float(self.delay_settings.noaudio_failover_delay)
        self._inhibit_switching_until = time_now

        self.stream = self.bind()
        self.frame_decoder = ZMQFrameDecoder()

    def __str__(self):
        return '<StreamInput: port {}>'.format(self.port)

    def bind(self):
        """
        bind zmq input port
        """
        logger.info('Binding socket on port {} - no-data failover delay/recovery: {}s/{}s - no-audio failover delay/recovery: {}s/{}s'.format(
            self.port,
            self.delay_settings.nodata_failover_delay,
            self.delay_settings.nodata_recover_delay,
            self.delay_settings.noaudio_failover_delay,
            self.delay_settings.noaudio_recover_delay,
        ))
        s = self.zmq_ctx.socket(zmq.SUB)
        s.bind('tcp://*:{port}'.format(port=self.port))
        s.setsockopt(zmq.SUBSCRIBE, b"")
        self.connected = True
        return ZMQStream(s)

    def stop(self):
        logger.debug('Stopping socket on port {}'.format(self.port))
        # close zmq socket
        self.stream.close()
        self.connected = False

    def tick(self, msg):
        """
        triggered on every `on_recv` - used to track input availability.
        """
        time_now = time.time()

        # always load frame so that the audio levels are visible in the
        # telnet interface
        self.frame_decoder.load_frame(msg)

        if self._last_beat + self.delay_settings.nodata_failover_delay < time_now:
            inhibit_switching_until = time_now + self.delay_settings.nodata_recover_delay

            if inhibit_switching_until > self._inhibit_switching_until:
                logger.debug("Input {} inhibit until {} because nodata".format(self.port,
                    time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(inhibit_switching_until))))

            self._inhibit_switching_until = max(self._inhibit_switching_until, inhibit_switching_until)

        if self._last_audio_ok + self.delay_settings.noaudio_failover_delay < time_now:
            inhibit_switching_until = time_now + self.delay_settings.noaudio_recover_delay

            if inhibit_switching_until > self._inhibit_switching_until:
                logger.debug("Input {} inhibit until {} because noaudio".format(self.port,
                    time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(inhibit_switching_until))))

            self._inhibit_switching_until = max(self._inhibit_switching_until, inhibit_switching_until)

        if self.delay_settings.audio_threshold != -90:
            audio_left, audio_right = self.frame_decoder.get_audio_levels()
            has_valid_audio = (audio_left is not None) and \
                              (audio_right is not None) and \
                              (audio_left > self.delay_settings.audio_threshold) and \
                              (audio_right > self.delay_settings.audio_threshold)
            if has_valid_audio:
                self._last_audio_ok = time_now
        else:
            # Assume audio is always ok
            self._last_audio_ok = time_now

        self._last_beat = time_now

    @property
    def is_available(self):
        """
        check if the input instance is 'available':
        "last time ticked less than failover duration"
        """
        time_now = time.time()
        has_recently_received_data = self._last_beat > (time_now - float(self.delay_settings.nodata_failover_delay))
        has_valid_audio = self._last_audio_ok > (time_now - float(self.delay_settings.noaudio_failover_delay))
        is_not_inhibited = self._inhibit_switching_until < time_now

        return has_recently_received_data and has_valid_audio and is_not_inhibited
