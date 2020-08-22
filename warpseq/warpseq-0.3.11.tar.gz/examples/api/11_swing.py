# --------------------------------------------------------------
# Warp API Demo
# (C) Michael DeHaan <michael@michaeldehaan.net>, 2020
# --------------------------------------------------------------
#
# demonstrates swing applied to a pattern using a transform, using the "sw" offset/swing mod expression
# this is clearer if shown on a single channel with both instruments unmuted.

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
api.instruments.add('lead_inst', device=DEVICE, channel=1, min_octave=0, base_octave=4, max_octave=10)

# ======================================================================================================================
# setup tracks

api.tracks.add(name='lead', instrument='lead_inst', muted=False)
api.tracks.add(name='reference', instrument='lead_inst', muted=False) # turn this off if you want

# ======================================================================================================================
# setup scales

api.scales.add(name='C-major', note='C', octave=0, scale_type='major')

# ======================================================================================================================
# setup transforms

api.transforms.add(name='drag', slots=[
    Slot(),
    Slot(),
    Slot(delay=0.1),
    Slot()
])

api.transforms.add(name='rush', slots=[
    Slot(),
    Slot(),
    Slot(delay=-0.1),
    Slot()
])

# setup patterns
api.patterns.add(name='up', length=16, rate=1, slots=[
    Slot(degree=4, length=0.5),
    Slot(degree=5, length=0.5),
    Slot(degree=6, length=0.5),
    Slot(degree=7, length=0.5)
])

api.patterns.add(name='beat', length=16, rate=1, slots=[
    Slot(note='C', octave=4),
    Slot(note='C', octave=4),
    Slot(note='C', octave=4),
    Slot(note='C', octave=4)
])

# ======================================================================================================================
# setup scenes

api.scenes.add(name='scene_1', scale='C-major', rate=0.5, auto_advance=True)
api.scenes.add(name='scene_2', scale='C-major', rate=0.5, auto_advance=True)
api.scenes.add(name='scene_END', scale='C-major', rate=0.5, auto_advance=True)

# ======================================================================================================================
# setup clips

api.clips.add(name='drag1', scene='scene_1', track='lead', patterns=['up'], transforms=['drag'], repeat=2, auto_scene_advance=True)
api.clips.add(name='reference1', scene='scene_1', track='reference', patterns=['beat'], repeat=None)

api.clips.add(name='rush1', scene='scene_2', track='lead', patterns=['up'], transforms=['rush'], repeat=2, auto_scene_advance=True)
api.clips.add(name='reference2', scene='scene_2', track='reference', patterns=['beat'], repeat=None)

# ======================================================================================================================
# play starting on the first scene - Ctrl+C to exit.

api.player.loop('scene_1')