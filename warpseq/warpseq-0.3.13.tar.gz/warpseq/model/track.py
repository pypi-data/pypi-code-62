# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# a track is a vertical row of clips that share a common instrument.
# a track can also be muted.

from .base import NewReferenceObject
from .instrument import Instrument

ALL_INSTRUMENTS = 'all_instruments'
ROTATE = 'rotate'
ROTATE_CHORDS = 'rotate_chords'
SPREAD = 'spread'
INSTRUMENT_MODE_CHOICES = [ ALL_INSTRUMENTS, ROTATE, ROTATE_CHORDS, SPREAD ]

class Track(NewReferenceObject):

    __slots__ = [ 'name', 'muted', 'instruments', 'clip_ids', 'obj_id', 'instrument_mode' ]

    SAVE_AS_REFERENCES = [ 'instruments' ]

    def __init__(self, name=None, muted=False, instrument=None, instruments=None, instrument_mode=ALL_INSTRUMENTS, clip_ids=None, obj_id=None):

        self.name = name
        self.muted = muted
        self.obj_id = obj_id

        if not instruments and instrument:
            instruments = [ instrument ]
        if instruments is None:
            instruments = []

        self.instruments = instruments

        if instrument_mode is None:
            instrument_mode = ALL_INSTRUMENTS

        self.instrument_mode = instrument_mode

        assert instrument_mode in INSTRUMENT_MODE_CHOICES

        if clip_ids is None:
            clip_ids = []
        self.clip_ids = clip_ids

        super(Track, self).__init__()


    def get_instruments_to_play(self):
        return self.instruments

    def has_clip(self, clip):
        return clip.obj_id in self.clip_ids

    def add_clip(self, clip):
        if clip.obj_id not in self.clip_ids:
            self.clip_ids.append(clip.obj_id)

    def remove_clip(self, clip):
        self.clip_ids = [ c for c in self.clip_ids if c != clip.obj_id ]

