# --------------------------------------------------------------
# Warp API Demo
# (C) Michael DeHaan <michael@michaeldehaan.net>, 2020
# --------------------------------------------------------------

# skipping notes, here done with probability in one example
# and a transform in another! a good chance to review
# transforms and what happens when a transform is of a different
# length from a pattern

# while they are here, the two instruments do NOT need to be on the same midi device!

from warpseq.api import demo
from warpseq.api.public import Api as WarpApi
from warpseq.model.slot import Slot, DataSlot
from warpseq.model.evaluator import Probability, DataGrab

# ======================================================================================================================
# setup API and song
api = WarpApi()
api.song.edit(tempo=60)

# ======================================================================================================================
# setup instruments

DEVICE = demo.suggest_device(api, 'IAC Driver IAC Bus 1')
api.instruments.add('one_instrument', device=DEVICE, channel=1, min_octave=0, base_octave=4, max_octave=10)

# ======================================================================================================================
# setup tracks
# notice 'instruments' vs 'instrument' here.
# it is legal to pass one instrument in an array to 'instruments', but it must take a list.

api.tracks.add(name='lead', instruments=['one_instrument'], muted=False)
api.scales.add(name='C-major', note='C', octave=0, scale_type='major')

# ======================================================================================================================
# setup transforms
#
# this transform skips every 3rd note, but because the other transform has even length this will skip different
# notes each time

api.transforms.add(name='skip_every_third', slots=[
    Slot(),
    Slot(),
    Slot(skip=1)
])

# ======================================================================================================================
# setup patterns

# the 1st note has a 50% chance of not playing and skipping 2 notes
# the 4th note has a 40% chance of skipping 3 notes
# but the 5th note has a 50% chance of skipping exactly one note and a 25% chance of skipping two

api.patterns.add(name='seq1', slots=[
    Slot(degree=1, octave_shift=2, skip=Probability(0.50, 2, 0)),
    Slot(degree=2),
    Slot(degree=3),
    Slot(degree=4, skip=Probability(0.40, 1, 0)),
    Slot(degree=5),
    Slot(degree=6),
    Slot(degree=7)
])

# just a basic pattern, but a transform will be applied
api.patterns.add(name='seq2', slots=[
    Slot(degree=1, octave_shift=2, chord_type='major'),
    Slot(degree=2),
    Slot(degree=3),
    Slot(degree=4),
    Slot(degree=5),
    Slot(degree=6),
    Slot(degree=7)
])

# a pattern that pulls the distance to skip from a data pool
api.patterns.add(name='seq3', slots=[
    Slot(degree=1, octave_shift=2, chord_type='major'),
    Slot(degree=2),
    Slot(degree=3),
    Slot(degree=4),
    Slot(degree=5, skip=DataGrab('skip_distance')),
    Slot(degree=6),
    Slot(degree=7)
])

# a pattern that pulls the probability of skipping from a data pool and also the distance!
api.patterns.add(name='seq4', slots = [
    Slot(degree=1, octave_shift=2, chord_type='major'),
    Slot(degree=2),
    Slot(degree=3),
    Slot(degree=4),
    Slot(degree=5, skip=Probability(DataGrab('skip_chance'), DataGrab('skip_distance'), 0)),
    Slot(degree=6),
    Slot(degree=7)
])


# ======================================================================================================================
# setup data pools

api.data_pools.add(name='skip_distance', slots=[
    DataSlot(value=0),
    DataSlot(value=0),
    DataSlot(value=1),
    DataSlot(value=2)
])

api.data_pools.add(name='skip_chance', slots=[
    DataSlot(value=0),
    DataSlot(value=0),
    DataSlot(value=0.5),
    DataSlot(value=1)
])

# ======================================================================================================================
# setup scenes

api.scenes.add(name='scene_1', rate=1, auto_advance=True)
api.scenes.add(name='scene_2', rate=1, auto_advance=True)
api.scenes.add(name='scene_3', rate=1, auto_advance=True)
api.scenes.add(name='scene_4', rate=1, auto_advance=True)

# ======================================================================================================================
# setup clips
api.clips.add(name='basic chance skips', scene='scene_1', track='lead', scales=['C-major'],
              patterns=['seq1'], repeat=8, auto_scene_advance=True)

api.clips.add(name='every third skips with transform', scene='scene_2', track='lead', scales=['C-major'],
              patterns=['seq2'], transforms=['skip_every_third'], repeat=8, auto_scene_advance=True)

api.clips.add(name='skip happens on 4th repeat using data pattern', scene='scene_3', track='lead', scales=['C-major'],
              patterns=['seq3'], repeat=8, auto_scene_advance=True)

api.clips.add(name='skip chance is pulled from a data pattern', scene='scene_4', track='lead', scales=['C-major'],
              patterns=['seq4'], repeat=8, auto_scene_advance=True)

# ======================================================================================================================
# play starting on the first scene - Ctrl+C to exit.

api.player.loop('scene_1')