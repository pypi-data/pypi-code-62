# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# a device represents a physical or virtual MIDI interface

from .base import NewReferenceObject
from warpseq.playback.midi import open_port

class Device(NewReferenceObject):

    __slots__ = [ 'name', 'obj_id', '_midi_out', ]

    SAVE_AS_REFERENCES = []

    def __init__(self, name=None, obj_id=None):
        self.name = name
        self.obj_id = obj_id
        self._midi_out = None
        super(Device,self).__init__()

    def get_midi_out(self):
        if self._midi_out is None:
            self._midi_out = open_port(self.name)
        return self._midi_out
