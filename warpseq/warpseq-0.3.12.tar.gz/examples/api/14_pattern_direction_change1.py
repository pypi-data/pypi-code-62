# --------------------------------------------------------------
# Warp API Demo
# (C) Michael DeHaan <michael@michaeldehaan.net>, 2020
# --------------------------------------------------------------
#
# shows how to use probability events to cause pattern
# resets (skipping to the start of a pattern), reshuffling,
# and reversing as a pattern runs.

from warpseq.api import demo
from warpseq.api.public import Api as WarpApi
from warpseq.model.slot import Slot
from warpseq.model.evaluator import Probability

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

api.patterns.add(name='resetting', slots=[
    Slot(degree=1),
    Slot(degree=2),
    Slot(degree=3),
    Slot(degree=4, reset=Probability(0.6, True, False)),
    Slot(degree=5),
    Slot(degree=6),
    Slot(degree=7),
    Slot(degree=8)
])

api.patterns.add(name='shuffling', slots=[
    Slot(degree=1),
    Slot(degree=2),
    Slot(degree=3),
    Slot(degree=4, shuffle=Probability(0.6, True, False)),
    Slot(degree=5),
    Slot(degree=6),
    Slot(degree=7),
    Slot(degree=8)
])

api.patterns.add(name='reversing', slots=[
    Slot(degree=1),
    Slot(degree=2),
    Slot(degree=3),
    Slot(degree=4, reverse=Probability(0.6, True, False)),
    Slot(degree=5),
    Slot(degree=6),
    Slot(degree=7),
    Slot(degree=8)
])

#=======================================================================================================================
# setup scenes

api.scenes.add(name='scene_1', rate=1, auto_advance=True)
api.scenes.add(name='scene_2', rate=1, auto_advance=True)
api.scenes.add(name='scene_3', rate=1, auto_advance=True)

#=======================================================================================================================
# setup clips

api.clips.add(name='reset demo', scene='scene_1', track='lead', scales=['C-major'], patterns=['resetting'],
              transforms=[], repeat=8, auto_scene_advance=True)

api.clips.add(name='shuffle demo', scene='scene_2', track='lead', scales=['C-major'], patterns=['shuffling'],
              transforms=[], repeat=8, auto_scene_advance=True)

api.clips.add(name='reverse demo', scene='scene_3', track='lead', scales=['C-major'], patterns=['reversing'],
              transforms=[], repeat=8, auto_scene_advance=True)

#=======================================================================================================================
# play starting on the first scene - Ctrl+C to exit.

api.player.loop('scene_1')