# --------------------------------------------------------------
# Warp API Demo
# (C) Michael DeHaan <michael@michaeldehaan.net>, 2020
# --------------------------------------------------------------

# this demo shows some other clip parameters, including
# scale changes and puts together some concepts mentioned
# in earlier demos. since all lists passed into the clip
# are different lengths, each repetition of the clip is different.

# fair warning: this isn't a very musical demo, it's more of a syntax
# demo of some obscure things you can put together

from warpseq.api import demo
from warpseq.api.public import Api as WarpApi
from warpseq.model.slot import Slot
from warpseq.model.evaluator import RandomChoice

# ======================================================================================================================
# setup API and song
api = WarpApi()
api.song.edit(tempo=60)

# ======================================================================================================================
# setup instruments
DEVICE = demo.suggest_device(api, 'IAC Driver IAC Bus 1')
api.instruments.add('lead_inst', device=DEVICE, channel=1, min_octave=0, base_octave=3, max_octave=10)

# ======================================================================================================================
# setup tracks
api.tracks.add(name='lead', instrument='lead_inst', muted=False)

# ======================================================================================================================
# setup scales
api.scales.add(name='C-major', note='C', octave=0, scale_type='major')
api.scales.add(name='F-mixolydian', note='F', octave=0, scale_type='mixolydian')
api.scales.add(name='magic', note='C', octave=0, slots=[1,4,5])

# ======================================================================================================================
# setup patterns
api.patterns.add(name='up', slots=[
    Slot(degree=1),
    Slot(degree=1),
    Slot(degree=1),
    Slot(rest=True),
    Slot(degree=4),
    Slot(degree=5),
    Slot(degree=6),
    Slot(degree=7),
    Slot(rest=True)
])
api.patterns.add(name='down', slots = [
    Slot(degree=6),
    Slot(degree=5),
    Slot(degree=4),
    Slot(degree=3),
    Slot(degree=2),
    Slot(degree=1)
])

# ======================================================================================================================
# setup transforms

# repeat each note quickly but add some gaps
api.transforms.add(name='stutter', divide=3, slots=[
    Slot(),
    Slot(),
    Slot(rest=True),
    Slot(),
    Slot()
])

# play multiple copies of notes + every fourth repeat has a 2 in 5 chance of jumping up 1 or 2 octaves
api.transforms.add(name='chance octave jump', divide=3, slots=[
    Slot(),
    Slot(),
    Slot(),
    Slot(octave_shift=RandomChoice(0,0,0,1,2))
])

# notes play at the same speed - every note jumps up an octave
api.transforms.add(name='octave up', divide=1, slots=[
    Slot(octave_shift=1)
])

# notes play at the same speed - every other note jumps up an octave
api.transforms.add(name='octave hop', divide=1, slots=[
    Slot(),
    Slot(octave_shift=1),
])

# notes play at the same speed - every third note jumps up a fifth vs what was in the original pattern
api.transforms.add(name='every third note up 5th', divide=1, slots=[
    Slot(),
    Slot(),
    Slot(degree_shift=5),
])

# ======================================================================================================================
# setup scenes
api.scenes.add(name='scene_1', rate=1, auto_advance=False)
api.scenes.add(name='scene_2', rate=1, auto_advance=False)

# ======================================================================================================================
# setup clips

api.clips.add(name='kitchen sink',
              scene='scene_1',
              track='lead',
              # each time we play a new pattern we will walk through using a different scale
              # after the third pattern this loops back around
              scales=[
                  'C-major',
                  'F-mixolydian',
                  'magic'
              ],
              patterns= [
                  'up',
                  'down'
              ],
              # each time we play a new pattern we will walk through and choose a new set of transforms
              # from this list. After the FOURTH pattern this will loop around
              transforms=[
                  ['octave up', 'stutter'],
                  ['octave hop', 'every third note up 5th'],
                  'chance octave jump'
              ],
              # each pattern goes a little faster than the previous (for a while, anyway, then it cycles)
              tempo_shifts = [
                  0,
                  5,
                  10,
                  15,
                  20,
                  25,
                  30
              ],
              # we'll play this same clip for a long time. Each repeat includes playing all of the patterns
              # so this means 8 total patterns will play
              repeat=4,
              # previous examples have shown the 'auto scene advance' feature, here we also show that we can jump
              # to specific clips in the same track if we don't use the scene advance
              next_clip='ending',
              rate=1)


# this is just a boring clip without using many clip features, but it does show the rate

api.clips.add(name='ending',
              scene='scene_2',
              track='lead',
              scales=['magic'],
              patterns=['down'],
              repeat=2,
              # this is part of our finale, so play it slower
              rate=0.25)

# play starting on the first scene - Ctrl+C to exit.
api.player.loop('scene_1')
