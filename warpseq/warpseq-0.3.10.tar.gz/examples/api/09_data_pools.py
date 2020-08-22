# --------------------------------------------------------------
# Warp API Demo
# (C) Michael DeHaan <michael@michaeldehaan.net>, 2020
# --------------------------------------------------------------
#
# this example shows one pattern where every step is spliced in using
# values from ANOTHER pattern
#
# these values replace the 4th note in the sequence each time they
# pass through
#
# additionally, velocity data for the last few notes in the pattern
# is pulled in from ANOTHER pattern that moves in a different direction (randomly
# serialized), showing patterns can be used for data and not just notes
#
# thus this lesson is an extension on some of the ideas on 08_directions.py

from warpseq.api import demo
from warpseq.api.public import Api as WarpApi
from warpseq.model.slot import Slot, DataSlot
from warpseq.model.evaluator import DataGrab

# ======================================================================================================================
# setup API and song

api = WarpApi()
api.song.edit(tempo=120)

# ======================================================================================================================
# setup instruments

DEVICE = demo.suggest_device(api, 'IAC Driver IAC Bus 1')

# ======================================================================================================================
# setup devices

api.instruments.add('lead_inst', device=DEVICE, channel=1, min_octave=0, base_octave=5, max_octave=10)

# ======================================================================================================================
# setup tracks

api.tracks.add(name='lead', instrument='lead_inst', muted=False)

# ======================================================================================================================
# setup scales

api.scales.add(name='C-major', note='C', octave=0, scale_type='major')
api.scales.add(name='F-pentatonic-minor', note='F', octave=0, scale_type='pentatonic_minor')

# ======================================================================================================================
# setup data pools

api.data_pools.add(name='sourceData', direction='random', slots=[
    DataSlot(value=1),
    DataSlot(value=2),
    DataSlot(value=3),
    DataSlot(value=4),
    DataSlot(value=5),
    DataSlot(value=6),
    DataSlot(value=7)
])

api.data_pools.add(name='vData', direction='pendulum', slots=[
    DataSlot(value=100),
    DataSlot(value=105),
    DataSlot(value=95),
    DataSlot(value=110),
    DataSlot(value=120)
])

# ======================================================================================================================
# setup patterns

api.patterns.add(name='play_this', direction='forward', slots=[
    Slot(degree=DataGrab('sourceData')),
    Slot(degree=DataGrab('sourceData')),
    Slot(degree=DataGrab('sourceData'), velocity=DataGrab('vData')),
    Slot(degree=6, velocity=DataGrab('vData')),
    Slot(degree=7, velocity=DataGrab('vData'))
])

# ======================================================================================================================
# setup scenes

api.scenes.add(name='scene_1', rate=1, auto_advance=True)
api.scenes.add(name='scene_END', rate=1, auto_advance=True)

# ======================================================================================================================
# setup clips

api.clips.add(name='repeated pattern with replacement from data pattern', scene='scene_1', track='lead',
              scales=['C-major'], patterns=['play_this'], repeat=8, auto_scene_advance=True, rate=0.5)

# ======================================================================================================================
# play starting on the first scene - Ctrl+C to exit.

api.player.loop('scene_1')