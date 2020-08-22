# --------------------------------------------------------------
# Warp API Demo
# (C) Michael DeHaan <michael@michaeldehaan.net>, 2020
# --------------------------------------------------------------
#
# the previous example teaches how to use 'reset', 'shuffle', and
# 'reverse' with probability.  This example shows how to use
# data pools to inject the probability from the outside, allowing
# the probability to change each time through the pattern.

from warpseq.api import demo
from warpseq.api.public import Api as WarpApi
from warpseq.model.slot import Slot, DataSlot
from warpseq.model.evaluator import *

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

# ======================================================================================================================
# setup scales

api.scales.add(name='C-major', note='F', octave=0, scale_type='major')

# ======================================================================================================================
# setup patterns

api.patterns.add(name='resetting', slots=[
    Slot(degree=1),
    Slot(degree=2),
    Slot(degree=3),
    Slot(degree=4, reset=Probability(DataGrab('build'), True, False)),
    Slot(degree=5),
    Slot(degree=6),
    Slot(degree=7),
])

api.patterns.add(name='shuffling', slots=[
    Slot(degree=1),
    Slot(degree=2),
    Slot(degree=3),
    Slot(degree=4, shuffle=Probability(DataGrab('rotatingChance'), True, False)),
    Slot(degree=5),
    Slot(degree=6),
    Slot(degree=7)
])

api.patterns.add(name='reversing', slots=[
    Slot(degree=1),
    Slot(degree=2),
    Slot(degree=3),
    Slot(degree=4, reverse=Probability(DataGrab('everyOther'), True, False)),
    Slot(degree=5),
    Slot(degree=6),
    Slot(degree=7)
])

# ======================================================================================================================
# now using data pools!

# note that multiple patterns can pull from the SAME data pool on multiple tracks, so that can
# sometimes be used for interesting effect. This is not demoed here.

# build is like 'forward', but the very last element repeats versus rolling back around
# once the end of the pattern is reached the probability will be 100!

api.data_pools.add(name='build', direction='build', slots=[
    DataSlot(value=0.05),
    DataSlot(value=0.1),
    DataSlot(value=0.5),
    DataSlot(value=0.9),
    DataSlot(value=1)
])

# the first pattern will never have the event happen, but the second
# pass through will have 50% chance, and the third pass will have 100! chance.

api.data_pools.add(name='rotatingChance', direction='forward', slots=[
    DataSlot(value=0.25),
    DataSlot(value=0.5),
    DataSlot(value=1)
])

# the first pattern will never have the event happen and the second pattern will
# happen with 100% chance

api.data_pools.add(name='everyOther', direction='forward', slots=[
    DataSlot(value=0),
    DataSlot(value=1)
])

# ======================================================================================================================
# setup scenes
api.scenes.add(name='scene_1', rate=1, auto_advance=True)
api.scenes.add(name='scene_2', rate=1, auto_advance=True)
api.scenes.add(name='scene_3', rate=1, auto_advance=True)

# ======================================================================================================================
# setup clips

api.clips.add(name='resetting demo (increasing odds)', scene='scene_1', track='lead', scales=['C-major'], patterns=['resetting'], transforms=[], repeat=8, auto_scene_advance=True)

api.clips.add(name='shuffling demo (randomly selected odds)', scene='scene_2', track='lead', scales=['C-major'], patterns=['shuffling'], transforms=[], repeat=8, auto_scene_advance=True)

api.clips.add(name='reversing demo (alternating toggle)', scene='scene_3', track='lead', scales=['C-major'], patterns=['reversing'], transforms=[], repeat=8, auto_scene_advance=True)

# ======================================================================================================================
# play starting on the first scene - Ctrl+C to exit.

api.player.loop('scene_1')


