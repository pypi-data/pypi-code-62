# -------------------------------------------------------------
# Warp API Demo
# (C) Michael DeHaan <michael@michaeldehaan.net>, 2020
# -------------------------------------------------------------
#
# this demo shows a basic 4/4 kick/snare pattern using absolute
# notes. It will not be adjusted by a scale assignment, which is
# important when talking to drum tracks.
#
# after the first basic pattern plays, the pattern changes up,
# showing how to advance a clip into a second scene.
#
# try changing the patterns and adding a third scene.

from warpseq.api import demo
from warpseq.api.public import Api as WarpApi
from warpseq.model.slot import Slot

# ======================================================================================================================
# setup API and song

api = WarpApi()
api.song.edit(tempo=120)

# ======================================================================================================================
# setup instruments

DEVICE = demo.suggest_device(api, 'IAC Driver IAC Bus 1')
api.instruments.add('kick_inst', device=DEVICE, channel=1, min_octave=0, base_octave=0, max_octave=10)
api.instruments.add('snare_inst', device=DEVICE, channel=2, min_octave=0, base_octave=0, max_octave=10)

# ======================================================================================================================
# setup tracks

api.tracks.add(name='kick', instrument='kick_inst', muted=False)
api.tracks.add(name='snare', instrument='snare_inst', muted=False)

# ======================================================================================================================
# setup patterns

api.patterns.add(name='kick_4_4', slots=[
   Slot(note='C', octave=1),
   Slot(rest=True),
   Slot(note='C', octave=1),
   Slot(rest=True)
])

api.patterns.add(name='snare_4_4', slots=[
   Slot(rest=True),
   Slot(note='D', octave=1),
   Slot(rest=True),
   Slot(note='D', octave=1)
])

# ======================================================================================================================
# setup scenes

api.scenes.add(name='scene_1', scale=None, auto_advance=True)

# ======================================================================================================================
# setup clips

api.clips.add(name='kick1', scene='scene_1', track='kick', patterns=['kick_4_4'], repeat=5, auto_scene_advance=True)
api.clips.add(name='snare1', scene='scene_1', track='snare', patterns=['snare_4_4'], repeat=5)

# ======================================================================================================================
# play starting on the first scene - Ctrl+C to exit.

api.player.loop('scene_1')
