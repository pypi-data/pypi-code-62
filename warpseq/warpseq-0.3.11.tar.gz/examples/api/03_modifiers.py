# --------------------------------------------------------------
# Warp API Demo
# (C) Michael DeHaan <michael@michaeldehaan.net>, 2020
# --------------------------------------------------------------
#
# this demo shows the different types of modifiers

from warpseq.api import demo
from warpseq.api.public import Api as WarpApi
from warpseq.model.slot import Slot
from warpseq.model.evaluator import Probability, RandomRange, RandomChoice

# ======================================================================================================================
# setup API and song
api = WarpApi()
api.song.edit(tempo=100)

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
api.scales.add(name='C-minor', note='C', octave=0, scale_type='natural_minor')

# ======================================================================================================================
# setup patterns
api.patterns.add(name='octave jumps', slots=[
    Slot(degree=1),
    Slot(degree=1, octave_shift=2),
    Slot(degree=1, octave_shift=-2),
    Slot(degree=5, octave_shift=2),
    Slot(degree=5, octave_shift=1),
    Slot(degree=5, octave_shift=-2)
])

api.patterns.add(name='sharps and flats', slots=[
    Slot(degree=1),
    Slot(degree=5),
    Slot(degree=4),
    Slot(degree=1, flat=True),
    Slot(degree=5, flat=True),
    Slot(degree=6, flat=True),
    Slot(degree=1, sharp=True),
    Slot(degree=3, sharp=True),
])

api.patterns.add(name='random octave jumps on certain steps', slots=[
    Slot(degree=1),
    Slot(degree=5, octave_shift=Probability(0.5, -1, 0)),
    Slot(degree=5, octave_shift=Probability(0.5, -1, 2)),
    Slot(degree=6),
    Slot(degree=4, octave_shift=Probability(0.5, 1, 0))
])

api.patterns.add(name='random flats on certain steps', slots=[
    Slot(degree=1),
    Slot(degree=5),
    Slot(degree=5, rest=Probability(0.5, True, False))
])

api.patterns.add(name='random octave jumps using a range', slots=[
    Slot(degree=1),
    Slot(degree=5),
    Slot(degree=4, octave=RandomRange(0,3)),
])

api.patterns.add(name='random octave jumps from a list', slots=[
    Slot(degree=1),
    Slot(degree=2),
    Slot(degree=4, octave=RandomChoice(0,1,2,3)),
    Slot(degree=5)
])

api.patterns.add(name='fixed MIDI velocity', slots=[
    Slot(degree=1),
    Slot(degree=5, velocity=80),
    Slot(degree=3, velocity=127),
    Slot(degree=4, velocity=60),
])

api.patterns.add(name='MIDI CC', slots=[
    Slot(degree=1, ccs={0: 40, 1:60}),
    Slot(degree=5),
    Slot(degree=4, ccs={1: RandomChoice(90,100), 2: RandomRange(100,120)}),
    Slot(degree=4, ccs={2: 90})
])

api.patterns.add(name='humanized MIDI velocity', slots=[
    Slot(degree=1),
    Slot(degree=2, velocity=RandomRange(80, 100)),
    Slot(degree=4, velocity=RandomRange(80, 100)),
    Slot(degree=5, velocity=RandomRange(80, 100)),
])

api.patterns.add(name='humanized MIDI CC', slots=[
    Slot(degree=1, ccs={0: RandomRange(40,100)}),
    Slot(degree=2),
    Slot(degree=3),
    Slot(degree=4),
]) # kind of like sample and hold!

api.patterns.add(name='randomized gaps', slots=[
    Slot(degree=1),
    Slot(degree=1, rest=Probability(0.5,True,False)),
    Slot(degree=1, rest=Probability(0.5, True, False)),
    Slot(degree=1, rest=Probability(0.5, True, False))
])

api.patterns.add(name='many things also with chords',slots=[
    Slot(degree=1, chord_type='major', ccs={1:50}, velocity=90, octave=RandomRange(0,3)),
    Slot(degree=4, chord_type='minor', ccs={1:75}, velocity=RandomRange(90,100)),
    Slot(degree=3, chord_type='power', velocity=RandomRange(90,100)),
    Slot(degree=4, chord_type='sus4', ccs={1:110}),
])

# ======================================================================================================================
# setup scenes

api.scenes.add(name='scene_1', rate=0.5, auto_advance=True)
api.scenes.add(name='scene_2', rate=0.5, auto_advance=True)
api.scenes.add(name='scene_3', rate=0.5, auto_advance=True)
api.scenes.add(name='scene_4', rate=0.5, auto_advance=True)
api.scenes.add(name='scene_5', rate=0.5, auto_advance=True)
api.scenes.add(name='scene_6', rate=0.5, auto_advance=True)
api.scenes.add(name='scene_7', rate=0.5, auto_advance=True)
api.scenes.add(name='scene_8', rate=0.5, auto_advance=True)
api.scenes.add(name='scene_9', rate=0.5, auto_advance=True)
api.scenes.add(name='scene_10', rate=0.5, auto_advance=True)
api.scenes.add(name='scene_11', rate=1, auto_advance=True)
api.scenes.add(name='scene_12', rate=0.5, auto_advance=True)

# ======================================================================================================================
# setup clips

api.clips.add(name='octave jumps', scene='scene_1', track='lead', scales=['C-major'],
              patterns=['octave jumps'], repeat=1, auto_scene_advance=True)

api.clips.add(name='sharps and flats', scene='scene_2', track='lead', scales=['C-major'],
              patterns=['sharps and flats'], repeat=1, auto_scene_advance=True)

api.clips.add(name='random octave jumps', scene='scene_3', track='lead', scales=['C-major'],
              patterns=['random octave jumps on certain steps'], repeat=4, auto_scene_advance=True)

api.clips.add(name='random flats', scene='scene_4', track='lead', scales=['C-major'],
              patterns=['random flats on certain steps'], repeat=4, auto_scene_advance=True)

api.clips.add(name='random octave jumps (range)', scene='scene_5', track='lead', scales=['C-major'],
              patterns=['random octave jumps using a range'], repeat=4, auto_scene_advance=True)

api.clips.add(name='random octave jumps (list)', scene='scene_6', track='lead', scales=['C-major'],
              patterns=['random octave jumps from a list'], repeat=4, auto_scene_advance=True)

api.clips.add(name='fixed MIDI velocity', scene='scene_7', track='lead', scales=['C-major'],
              patterns=['fixed MIDI velocity'], repeat=1, auto_scene_advance=True)

api.clips.add(name='randomized MIDI CC', scene='scene_8', track='lead', scales=['C-major'],
              patterns=['MIDI CC'], repeat=1, auto_scene_advance=True)

api.clips.add(name='humanized velocity', scene='scene_9', track='lead', scales=['C-major'],
              patterns=['humanized MIDI velocity'], repeat=4, auto_scene_advance=True)

api.clips.add(name='humanized CC', scene='scene_10', track='lead', scales=['C-major'],
              patterns=['humanized MIDI CC'], repeat=4, auto_scene_advance=True)

api.clips.add(name='randomized gaps', scene='scene_11', track='lead', scales=['C-major'],
              patterns=['randomized gaps'], repeat=8, auto_scene_advance=True)

api.clips.add(name='many things also with chords', scene='scene_12', track='lead', scales=['C-major'],
              patterns=['many things also with chords'], repeat=4, auto_scene_advance=True)

# ======================================================================================================================
# play starting on the first scene - Ctrl+C to exit.

api.player.loop('scene_1')
