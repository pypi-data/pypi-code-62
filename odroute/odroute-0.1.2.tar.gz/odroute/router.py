# -*- coding: utf-8 -*-
import logging
import sys
import zmq

from functools import partial
from zmq.eventloop import ioloop
from collections import namedtuple

from .input import StreamInput
from .output import StreamOutput
from .utils import index_by_dict_key, index_by_obj_prop
from .config import load_config_file
from .frame import ZMQFrameDecoder

logger = logging.getLogger(__name__)

ioloop.install()


class StreamRouter(object):
    """
    Router instance. Handles input and output connections & routing (priority).
    """
    # `_source_ports` and `_destinations` are only used for initial router setup (during instance `start`)
    _source_ports = []
    _destinations = []
    _inputs = []
    _current_input = None
    _last_input = None
    _forced_port = None
    _outputs = []
    _current_config = None
    _state = None
    _start_with_ioloop = []
    _state_change_callbacks = []

    DelaySettings = namedtuple('DelaySettings', [
        'nodata_failover_delay',
        'nodata_recover_delay',
        'noaudio_failover_delay',
        'noaudio_recover_delay',
        'audio_threshold'])

    def __init__(self, config, **options):
        self._current_config = config

        self._source_ports = config.get('source_ports')
        self._destinations = config.get('destinations')

        self.delay_settings = StreamRouter.DelaySettings(
                config.get('nodata_failover_delay'),
                config.get('nodata_recover_delay'),
                config.get('noaudio_failover_delay'),
                config.get('noaudio_recover_delay'),
                config.get('audio_threshold'))

        self.zmq_ctx = zmq.Context()

    def get_current_input(self):
        return self._current_input

    def set_auto_switch(self):
        self._forced_port = None

    def force_input(self, i):
        if i not in [inp.port for inp in self._inputs]:
            raise ValueError("Port {} not available".format(i))
        self._forced_port = i





    ###################################################################
    # input a.k.a. source handling
    ###################################################################
    def add_input(self, port, before=False):
        i = StreamInput(self.zmq_ctx, port, self.delay_settings)
        if before:
            self._inputs.insert(0, i)
        else:
            self._inputs.append(i)
        logger.info('Created input socket on port {}'.format(port))


    def remove_input(self, port):
        index = index_by_obj_prop(self._inputs, 'port', port)
        if index > -1:
            i = self._inputs.pop(index)
            i.stop()
        logger.info('Removed input socket on port {}'.format(port))

    def get_inputs(self):
        return self._inputs

    def get_input_ports(self):
        return [i.port for i in self._inputs]





    ###################################################################
    # output a.k.a. destination handling
    ###################################################################
    def add_output(self, destination):
        o = StreamOutput(self.zmq_ctx, destination)
        logger.info('Connected output to {}'.format(destination))
        self._outputs.append(o)

    def remove_output(self, destination):
        index = index_by_obj_prop(self._outputs, 'output', destination)
        if index > -1:
            o = self._outputs.pop(index)
            o.stop()
        logger.info('Removed output to {}'.format(destination))

    def get_outputs(self):
        return self._outputs

    def get_output_destinations(self):
        return [o.output for o in self._outputs]


    def set_current_input(self):
        current_input = None

        if not self._inputs:
            self._current_input = None
            return
        elif len(self._inputs) == 1:
            # Avoid switching to None if the only input is not-available.
            # There is no need for any flapping protection anyway in this case.
            current_input = self._inputs[0]

        # force input
        if self._forced_port:
            filtered_inputs = [i for i in self._inputs if i.port == self._forced_port]
            if filtered_inputs:
                current_input = filtered_inputs[0]

        # Loop through the inputs and return the first available one.
        if not current_input:
            available_inputs = [i for i in self._inputs if i.is_available]
            if available_inputs:
                current_input = available_inputs[0]

        self._current_input = current_input

        if current_input != self._last_input:
            logger.info('Switching inputs: {} to {}'.format(
                self._last_input.port if self._last_input else None,
                current_input.port if current_input else None))
            self._last_input = current_input


    def route(self, stream, msg, input):
        """
        Routes the active input to all outputs
        """

        frame_decoder = ZMQFrameDecoder()
        frame_decoder.load_frame(msg[0])
        if not frame_decoder.is_valid():
            logger.warn("Invalid frame of length {} received, ignored.".format(len(msg[0])))
            return

        # Trigger a 'heartbeat' tick on the input.
        input.tick(msg[0])

        self.set_current_input()

        if input == self._current_input:
            for o in self._outputs:
                o.send(msg[0])

    def start(self):

        for port in self._source_ports:
            self.add_input(port=port)
        self._source_ports = []

        for destination in self._destinations:
            self.add_output(destination)
        self._destinations = []

        for i in self._inputs:
            i.stream.on_recv_stream(partial(self.route, input=i))

        for cb in self._start_with_ioloop:
            if not cb.started:
                logger.debug('Starting with ioloop: {}'.format(cb))
                cb.start()

        # Initialise the tornado ioloop
        # http://pyzmq.readthedocs.io/en/latest/eventloop.html#futures-and-coroutines
        io_loop = ioloop.IOLoop.instance()

        io_loop.start()

        while True:
            pass

    def stop(self):
        logger.info('Stopping router')
        for port in self.get_input_ports():
            self.remove_input(port=port)

        for destination in self.get_output_destinations():
            self.remove_output(destination)

        sys.exit()

    def register_start_with_ioloop(self, cb):
        if not cb in self._start_with_ioloop:
            self._start_with_ioloop.append(cb)

    def reload_configuration(self):
        config_file = self._current_config.get('config_file')
        config = load_config_file(config_file)

        self.delay_settings = StreamRouter.DelaySettings(
                config.get('nodata_failover_delay'),
                config.get('nodata_recover_delay'),
                config.get('noaudio_failover_delay'),
                config.get('noaudio_recover_delay'),
                config.get('audio_threshold'))

        ###############################################################
        # reconfigure outputs, a.k.a. 'destinations'
        ###############################################################
        current_destinations = self.get_output_destinations()
        new_destinations = config.get('destinations')

        # stop removed outputs
        for destionation in current_destinations:
            if not destionation in new_destinations:
                self.remove_output(destionation)

        # add newly configured outputs
        for destionation in new_destinations:
            if not destionation in current_destinations:
                self.add_output(destionation)



        ###############################################################
        # reconfigure inputs, a.k.a. 'source_ports'
        ###############################################################
        current_input_ports = self.get_input_ports()
        new_input_ports = config.get('source_ports')

        # stop removed inputs
        for port in current_input_ports:
            if not port in new_input_ports:
                self.remove_input(port)

        # add newly configured inputs
        for port in new_input_ports:
            if not port in current_input_ports:
                self.add_input(port)

        # update order / priority of inputs
        # TODO: 100% sure there is a better way to implement this :)
        _inputs = []
        for port in new_input_ports:
            for i in self._inputs:
                if i.port == port:
                    _inputs.append(i)

        # replace inputs with updated/sorted values
        self._inputs = _inputs

