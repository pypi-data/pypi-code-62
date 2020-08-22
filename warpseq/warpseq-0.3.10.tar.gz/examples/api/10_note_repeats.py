# --------------------------------------------------------------
# Warp API Demo
# (C) Michael DeHaan <michael@michaeldehaan.net>, 2020
# --------------------------------------------------------------
#
# demonstrates repeated notes, which are a useful feature for accents ("r=")
# also demonstrates length mods ("l="), which can be used to make dotted notes and half-length notes
# record this MIDI in your DAW and you can better see what is going on, but it should be decently obvious from just listening

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
api.instruments.add('lead_inst', device=DEVICE, channel=1, min_octave=0, base_octave=5, max_octave=10)

# ======================================================================================================================
# setup tracks

api.tracks.add(name='lead', instrument='lead_inst', muted=False)

# ======================================================================================================================
# setup scales

api.scales.add(name='C-major', note='C', octave=0, scale_type='major')

# ======================================================================================================================
# setup patterns

api.patterns.add(name='up', slots=[
    Slot(degree=1, chord_type='major', repeats=8),
    Slot(degree=2),
    Slot(degree=3, repeats=2), #length=1.5),
    Slot(rest=True),
    Slot(degree=5, repeats=4),
    Slot(degree=1),
    Slot(degree=2),
    Slot(rest=True),
    Slot(degree=4),
    Slot(degree=5),
    Slot(degree=4, chord_type='major', repeats=3),
    Slot(degree=1),
    Slot(degree=2),
    Slot(degree=3),
    Slot(degree=5, chord_type='major', repeats=3),
    Slot(degree=1),
    Slot(degree=2),
    Slot(degree=3),
    Slot(degree=1, chord_type='major', repeats=6),
    Slot(tie=True),
    Slot(tie=True)
])

# ======================================================================================================================
# setup scenes

api.scenes.add(name='scene_1', rate=0.5, auto_advance=True)

# ======================================================================================================================
# setup clips

api.clips.add(name='repeat and length demo', scene='scene_1', track='lead', scales=['C-major'], patterns=['up'],
              repeat=4, auto_scene_advance=True)

# ======================================================================================================================
# play starting on the first scene - Ctrl+C to exit.

api.player.loop('scene_1')