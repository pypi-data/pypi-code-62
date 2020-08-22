# --------------------------------------------------------------
# Warp API Demo
# (C) Michael DeHaan <michael@michaeldehaan.net>, 2020
# --------------------------------------------------------------

# this is a super basic example that shows we can send notes to multiple tracks,
# for instance you could send notes to two polysynths, once with a long pad
# sound and another with a sharper attack.

# while they are here, the two instruments do NOT need to be on the same midi device!

from warpseq.api import demo
from warpseq.api.public import Api as WarpApi
from warpseq.model.slot import Slot, DataSlot
from warpseq.model.evaluator import *

# ======================================================================================================================
# setup API and song

api = WarpApi()
api.song.edit(tempo=60)

# ======================================================================================================================
# setup instruments

DEVICE = demo.suggest_device(api, 'IAC Driver IAC Bus 1')
api.instruments.add('doc', device=DEVICE, channel=1, min_octave=0, base_octave=3, max_octave=10, muted=False)
api.instruments.add('happy', device=DEVICE, channel=2, min_octave=0, base_octave=3, max_octave=10, muted=False)
api.instruments.add('sneezy', device=DEVICE, channel=3, min_octave=0, base_octave=3, max_octave=10, muted=False)
api.instruments.add('sleepy', device=DEVICE, channel=4, min_octave=0, base_octave=3, max_octave=10, muted=False)
api.instruments.add('bashful', device=DEVICE, channel=5, min_octave=0, base_octave=3, max_octave=10, muted=False)
api.instruments.add('grumpy', device=DEVICE, channel=6, min_octave=0, base_octave=3, max_octave=10, muted=False)
api.instruments.add('dopey', device=DEVICE, channel=7, min_octave=0, base_octave=3, max_octave=10, muted=False)

# ======================================================================================================================
# setup tracks

# notice 'instruments' vs 'instrument' here.
# it is legal to pass one instrument in an array to 'instruments', but it must take a list.

all_the_dwarves = [ 'doc', 'happy', 'sneezy', 'sleepy', 'bashful', 'grumpy', 'dopey' ]

# all instruments is the default
api.tracks.add(name='all instruments', instruments=all_the_dwarves, instrument_mode='all_instruments', muted=False)

# distribute each note to the next instrument in the list
api.tracks.add(name='rotate', instruments=all_the_dwarves, instrument_mode='rotate', muted=False)

# distribute each chord to the next instrument in the list
api.tracks.add(name='rotate chords', instruments=all_the_dwarves, instrument_mode='rotate_chords', muted=False)

# play one note of each chord among the first N synths in the list
api.tracks.add(name='spread', instruments=all_the_dwarves, instrument_mode='spread', muted=False)


# ======================================================================================================================
# setup scales

api.scales.add(name='C-major', note='C', octave=0, scale_type='major')

# ======================================================================================================================
# setup patterns

api.patterns.add(name='chords', slots=[
    Slot(degree=1, chord_type='major'),
    Slot(degree=4, chord_type='major'),
    Slot(degree=5, chord_type='major'),
    Slot(degree=7, chord_type='major')
])

# ======================================================================================================================
# setup scenes

api.scenes.add(name='scene_1', rate=0.5, auto_advance=True)
api.scenes.add(name='scene_2', rate=0.5, auto_advance=True)
api.scenes.add(name='scene_3', rate=0.5, auto_advance=True)
api.scenes.add(name='scene_4', rate=0.5, auto_advance=True)

# ======================================================================================================================

# setup clips
api.clips.add(name='s1a', scene='scene_1', track='all instruments', scales=['C-major'],
              patterns=['chords'], repeat=4, auto_scene_advance=True)

api.clips.add(name='s2a', scene='scene_2', track='rotate', scales=['C-major'],
              patterns=['chords'], repeat=4, auto_scene_advance=True)

api.clips.add(name='s3a', scene='scene_3', track='rotate chords', scales=['C-major'],
              patterns=['chords'], repeat=4, auto_scene_advance=True)

api.clips.add(name='s4a', scene='scene_4', track='spread', scales=['C-major'],
              patterns=['chords'], repeat=4, auto_scene_advance=True)

# ======================================================================================================================
# play starting on the first scene - Ctrl+C to exit.

api.player.loop('scene_1')