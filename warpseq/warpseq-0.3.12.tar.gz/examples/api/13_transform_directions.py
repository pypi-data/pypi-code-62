# --------------------------------------------------------------
# Warp API Demo
# (C) Michael DeHaan <michael@michaeldehaan.net>, 2020
# --------------------------------------------------------------
#
# our examples have been getting dense and it's time for a break.
# let's refresh your memory about that last example while
# doing some recap about transforms being used as arpeggiators.
#
# here is a simple example of transform directions that how to
# transform the input notes at random
#
# we also mix in "length" and "repeat" to make it more interesting
#
# record the MIDI from this one and see what is going on

from warpseq.api import demo
from warpseq.api.public import Api as WarpApi
from warpseq.model.slot import Slot

#=======================================================================================================================
# setup API and song

api = WarpApi()
api.song.edit(tempo=120)

#=======================================================================================================================
# setup instruments

DEVICE = demo.suggest_device(api, 'IAC Driver IAC Bus 1')
api.instruments.add('lead_inst', device=DEVICE, channel=1, min_octave=0, base_octave=4, max_octave=10)

#=======================================================================================================================
# setup tracks

api.tracks.add(name='lead', instrument='lead_inst', muted=False)

#=======================================================================================================================
# setup scales

api.scales.add(name='C-major', note='F', octave=0, scale_type='major')

#=======================================================================================================================
# setup patterns

api.patterns.add(name='chords', slots=[
    Slot(degree=1, chord_type='major'),
    Slot(degree=1, chord_type='major'),
    Slot(degree=5, chord_type='major'),
])

#=======================================================================================================================
# setup transforms
# try other directions - pendulum, reverse, brownian1, brownian2, ... brownian6, etc.

api.transforms.add(name='shift', divide=None, direction='random', slots=[
    Slot(),
    Slot(degree_shift=4),
    Slot(degree_shift=5),
    Slot(octave_shift=1),
    Slot(repeats=4),
    Slot(length=0.5)
])

#=======================================================================================================================
# setup scenes

api.scenes.add(name='scene_1', rate=0.25, auto_advance=True)

#=======================================================================================================================
# setup clips

api.clips.add(name='s1c', scene='scene_1', track='lead', scales=['C-major'], patterns=['chords'], transforms=['shift'], repeat=6, auto_scene_advance=True)

#=======================================================================================================================
# play starting on the first scene - Ctrl+C to exit.

api.player.loop('scene_1')