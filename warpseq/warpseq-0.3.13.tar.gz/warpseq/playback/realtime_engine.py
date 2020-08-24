# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# this class is used by the player code to send MIDI events to hardware
# it contains some logic to convert chords to note events and must also
# process deferred mod-expressions caused by late-binding intra-track
# events.

from warpseq.api.callbacks import Callbacks
from warpseq.api.exceptions import *
from warpseq.model.registers import register_playing_note, unregister_playing_note
from warpseq.playback.midi import midi_note_on, midi_note_off, midi_cc
from warpseq.model.chord import Chord
from warpseq.model.event import Event, NOTE_OFF, NOTE_ON
from warpseq.model.track import ALL_INSTRUMENTS, ROTATE, SPREAD, ROTATE_CHORDS
from warpseq.utils import utils

# ======================================================================================================================

def _get_note_number(note, instrument):

    max_o = instrument.max_octave
    min_o = instrument.min_octave

    note2 = note.copy().transpose(octaves=instrument.base_octave)

    if note2.octave > max_o:
        note2.octave = max_o
    if note2.octave < min_o:
        note2.octave = min_o

    nn = note2.note_number()

    if nn < 0 or nn > 127:
        print("warning: note outside of playable range: %s" % note)
        return None

    return nn

# ======================================================================================================================

class RealtimeEngine(object):

    __slots__ = ['song','track','clip','midi_out','midi_port','mod_expressions','callbacks','on_count','player',
                 '_all_instruments', '_instruments_roller', '_hocket_roller', '_poly_roller']

    # ------------------------------------------------------------------------------------------------------------------


    def __init__(self, song=None, track=None, clip=None, player=None):
        self.song = song
        self.track = track
        self.clip = clip
        self.player = player
        self.callbacks = Callbacks()

        self._all_instruments = self.track.get_instruments_to_play()
        self._hocket_roller = utils.roller(self._all_instruments)

    # ------------------------------------------------------------------------------------------------------------------

    def _get_instruments(self, evt, chosen, instrument_mode):
        if instrument_mode == ALL_INSTRUMENTS:
            return self._all_instruments
        elif instrument_mode in [ROTATE_CHORDS, SPREAD]:
            return [next(self._hocket_roller)]
        elif instrument_mode == ROTATE:
            return [chosen]
        else:
            raise Exception("unknown mode")

    # ------------------------------------------------------------------------------------------------------------------

    def _process_deferred(self, evt):

        exprs = evt.note.deferred_expressions
        for expr in exprs:
            value = expr.evaluate(self.track, evt.note)
            if value is None:
                return
            evt.note = value

    # ------------------------------------------------------------------------------------------------------------------

    def _before_instrument_select(self, instrument_mode):

        if instrument_mode == SPREAD:
            self._hocket_roller = utils.roller(self._all_instruments)
        if instrument_mode == ROTATE:
            return next(self._hocket_roller)
        return None

    # ------------------------------------------------------------------------------------------------------------------

    def _play_notes(self, event):

        mode = self.track.instrument_mode
        chosen = self._before_instrument_select(mode)
        for (i, x) in enumerate(event.note.notes):
            if x.muted:
                return
            evt = event.copy()
            evt.note = x
            evt.instruments = self._get_instruments(evt, chosen, mode)
            self._process_deferred(evt)
            self.play(evt)

    # ------------------------------------------------------------------------------------------------------------------

    def _play_note_on(self, event):

        velocity = event.note.velocity
        if velocity is None:
            velocity = self.instrument.default_velocity

        register_playing_note(self.track, event.note)

        for (control, value) in event.note.ccs.items():
            control = int(control)
            for instrument in event.get_instruments():
                midi_cc(instrument.get_midi_out(), instrument.channel, control, int(value))

        if not (self.track.muted or event.note.muted):

            self.player.inject_off_event(event)

            for instrument in event.get_instruments():
                if not instrument.muted:
                    # print("PLAY ON %s: %s" % (self.track.name, event.note))
                    midi_note_on(instrument.get_midi_out(), instrument.channel,
                                 _get_note_number(event.note, instrument), velocity)

    # ------------------------------------------------------------------------------------------------------------------

    def _play_note_off(self, event):

        unregister_playing_note(self.track, event.on_event.note)

        if self.track.muted:
            return

        velocity = event.note.velocity
        if velocity is None:
            velocity = self.instrument.default_velocity

        for instrument in event.get_instruments():
            if not instrument.muted:
                midi_note_off(instrument.get_midi_out(), instrument.channel,
                              _get_note_number(event.note, instrument), velocity)

    # ------------------------------------------------------------------------------------------------------------------

    def play(self, event):

        if not event.note:
            return
        if type(event.note) == Chord:
            self._play_notes(event)
            return
        if event.type == NOTE_ON:
            self._play_note_on(event)
        elif event.type == NOTE_OFF:
            self._play_note_off(event)
        else:
            raise Exception("???")


