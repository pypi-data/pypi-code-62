# --------------------------------------------------------------
# Warp API Demo
# (C) Michael DeHaan <michael@michaeldehaan.net>, 2020
# --------------------------------------------------------------
#
# this demo shows how variables work, using them to control
# octave shifts, MIDI CC and velocity. Variables cannot
# have spaces in their names and are case insensitive.
#
# remember that variables are global and are accessible to all tracks
# it can be useful to set them on a muted guide track, and then access
# those values on different tracks.
#
# the first demo is audible, but the next two may not be depending on
# the configuration of your musical instruments - they would need
# to respond to MIDI velocity and CC data.
#
# to observe MIDI CC behavior, consider recording the MIDI
# stream and looking at it in your DAW.  Then tweak the
# patterns and see how things change.

from warpseq.api import demo
from warpseq.api.public import Api as WarpApi
from warpseq.model.slot import Slot
from warpseq.model.evaluator import LoadVariable, RandomRange, RandomChoice, Probability, Negate

# ======================================================================================================================
# setup API and song

api = WarpApi()
api.song.edit(tempo=120)

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

# example 1:
#
# the octave shift is chosen for the pattern and the octave shift
# is applied to two notes in the pattern
# two different scale shift is also chosen and applied to different notes
# (because we have assigned a scale, everything still remains within the scale)

rr = RandomRange(1,4)
rr2 = RandomRange(0,2)

api.patterns.add(name='variables1', slots=[
    Slot(degree=4,
         chord_type='major',
         variables=dict(octaveShift=rr2, noteShift=rr, noteShiftB=rr),
         degree_shift=LoadVariable('noteShift')),
    Slot(degree=2),
    Slot(degree=4,
         degree_shift=LoadVariable('noteShiftB')),
    Slot(degree=6),
    Slot(degree=1,
         octave_shift=LoadVariable('octaveShift'),
         degree_shift=LoadVariable('noteShift')),
    Slot(degree=2,
         degree_shift=LoadVariable('noteShiftB')),
    Slot(degree=8,
         octave_shift=RandomChoice(LoadVariable('octaveShift'), 0, -1)),
    Slot(degree=4),
    Slot(degree=1,
         octave_shift=Probability(0.75, LoadVariable('octaveShift'), 1)),
    Slot(degree=1,
         octave_shift=RandomRange(0, LoadVariable('octaveShift')),
         degree_shift=Negate(LoadVariable('noteShift'))),
    Slot(degree=3)
])

# example 2:
#
# two MIDI CC values are selected randomly
# the first value is used on the quarter note beats
# the second value is used for all other beats
# because MIDI CCs are sticky we do not need to set them on every note
# the random values are recomputed each time the pattern changes

api.patterns.add(name='variables2', slots=[
    Slot(degree=4, chord_type='major', variables={'x':RandomRange(25,100), 'y':RandomRange(25,100)}, ccs={'1':LoadVariable('x')}),
    Slot(degree=2, ccs={1:LoadVariable('y')}),
    Slot(degree=3),
    Slot(degree=4),
    Slot(degree=1, ccs={1:LoadVariable('x')}),
    Slot(degree=2, ccs={1:LoadVariable('y')}),
    Slot(degree=3),
    Slot(degree=4)
])

# example 3:
#
# velocity values on quarter note beats are full strength
# in between, notes are one of two randomized values
# the randomized values change every pattern

api.patterns.add(name='variables3', slots=[
   Slot(degree=4, chord_type='major', velocity=127, variables={'a': RandomRange(20,40), 'b': RandomRange(90,100) }),
   Slot(degree=2, velocity=LoadVariable('a')),
   Slot(degree=3, velocity=LoadVariable('b')),
   Slot(degree=1, velocity=127),
   Slot(degree=2, velocity=LoadVariable('a')),
   Slot(degree=3, velocity=LoadVariable('b')),
   Slot(degree=4, velocity=50),
   Slot(degree=1, velocity=127),
   Slot(degree=2, velocity=LoadVariable('a')),
   Slot(degree=3, velocity=LoadVariable('b')),
   Slot(degree=4, velocity=50),
   Slot(degree=1, velocity=127),
   Slot(degree=2, velocity=LoadVariable('a')),
   Slot(degree=3, velocity=LoadVariable('b')),
   Slot(degree=4, velocity=40)
])

# ======================================================================================================================
# setup scenes

api.scenes.add(name='scene_1', rate=0.5, auto_advance=True)
api.scenes.add(name='scene_2', rate=0.5, auto_advance=True)
api.scenes.add(name='scene_3', rate=0.5, auto_advance=True)

# ======================================================================================================================
# setup clips

api.clips.add(name='s1c', scene='scene_1', track='lead', scales=['C-major'], patterns=['variables1'], repeat=8, auto_scene_advance=True)
api.clips.add(name='s2c', scene='scene_2', track='lead', scales=['C-major'], patterns=['variables2'], repeat=8, auto_scene_advance=True)
api.clips.add(name='s3c', scene='scene_3', track='lead', scales=['C-major'], patterns=['variables3'], repeat=8, auto_scene_advance=True)

# ======================================================================================================================
# play starting on the first scene - Ctrl+C to exit.
api.player.loop('scene_1')