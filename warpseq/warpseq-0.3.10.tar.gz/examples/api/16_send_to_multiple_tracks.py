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
from warpseq.model.slot import Slot

# ======================================================================================================================
# setup API and song

api = WarpApi()
api.song.edit(tempo=60)

# ======================================================================================================================
# setup instruments

DEVICE = demo.suggest_device(api, 'IAC Driver IAC Bus 1')
api.instruments.add('one_instrument', device=DEVICE, channel=1, min_octave=0, base_octave=4, max_octave=10)
api.instruments.add('another_instrument', device=DEVICE, channel=2, min_octave=0, base_octave=4     , max_octave=10)

# ======================================================================================================================
# setup tracks

# notice 'instruments' vs 'instrument' here.
# it is legal to pass one instrument in an array to 'instruments', but it must take a list.

api.tracks.add(name='one_single_track_with_two_instruments', instruments=['one_instrument','another_instrument'], muted=False)

api.scales.add(name='C-major', note='C', octave=0, scale_type='major')

# ======================================================================================================================
# setup patterns

api.patterns.add(name='chords', slots=[
    Slot(degree=1, chord_type='major'),
    Slot(degree=4, chord_type='major'),
    Slot(degree=5),
    Slot(degree=7)
])

# ======================================================================================================================
# setup scenes

api.scenes.add(name='scene_1', rate=0.5, auto_advance=True)

# ======================================================================================================================

# setup clips
api.clips.add(name='s1a', scene='scene_1', track='one_single_track_with_two_instruments', scales=['C-major'],
              patterns=['chords'], repeat=4, auto_scene_advance=True)

# ======================================================================================================================
# play starting on the first scene - Ctrl+C to exit.

api.player.loop('scene_1')