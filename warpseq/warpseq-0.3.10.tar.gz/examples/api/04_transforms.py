# --------------------------------------------------------------
# Warp API Demo
# (C) Michael DeHaan <michael@michaeldehaan.net>, 2020
# --------------------------------------------------------------
#
# this demo shows how transforms work (see docs!) and how
# to build a simple arpeggiator, as well as other MIDI effects.
#
# warning: as with all demos, whether these demos sound
# musical may vary based on your chosen instruments! These are mostly
# to illustrate concepts, and the compositions are up to you.

from warpseq.api import demo
from warpseq.api.public import Api as WarpApi
from warpseq.model.slot import Slot
from warpseq.model.evaluator import RandomRange, Probability

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

api.scales.add(name='C-major', note='C', octave=0, scale_type='major')
api.scales.add(name='C-minor', note='C', octave=0, scale_type='natural_minor')

# ======================================================================================================================
# setup patterns

api.patterns.add(name='basic', slots=[
    Slot(degree=1),
    Slot(degree=2),
    Slot(degree=3),
    Slot(degree=4),
    Slot(degree=5),
    Slot(degree=6),
    Slot(degree=7),
    Slot(degree=8)
])

api.patterns.add(name='chords', slots=[
    Slot(degree=1, chord_type='major'),
    Slot(rest=True),
    Slot(degree=4, chord_type='major'),
    Slot(rest=True),
    Slot(degree=5, chord_type='major'),
    Slot(rest=True)
])

# setup transforms
# arpeggiate chords only - auto-divide chords regardless of length so each 1/16 note plays each note in the chord.
# Triads will strum faster than power chords, etc.

api.transforms.add(name='basic arp', applies_to='chords', slots=[
    Slot()
])

# play two copies of the chord, the second one octave up
# the auto-reset flag means the transform always restarts cleanly at the start of each new pattern, which is useful if
# the transform is not of the same length but leaving auto_reset *OFF* can make for more interesting patterns as they
# repeat

api.transforms.add(name='octave arp', auto_reset=True, slots=[
    Slot(),
    Slot(),
    Slot(),
    Slot(octave_shift=1),
    Slot(octave_shift=1),
    Slot(octave_shift=1),
])

api.transforms.add(name='octave up', slots=[
    Slot(octave_shift=1),
    Slot(octave_shift=2)
])

# play each note in a triad with diminished velocity (this might not be audible, depending on your synth settings)
api.transforms.add(name='velocity arp', slots=[
    Slot(velocity=120),
    Slot(velocity=100),
    Slot(velocity=80),
])

# play each note in a triad with different MIDI CC values for MIDI CC 1
api.transforms.add(name='midi cc arp', slots=[
    Slot(ccs={1:80}),
    Slot(ccs={1:100}),
    Slot(ccs={1:RandomRange(20,100)})
])

# take the base note of a pattern and then play it faster, shifting the scale notes to form a bassline
api.transforms.add(name='bassline', divide=5, slots=[
    Slot(),
    Slot(degree_shift=4),
    Slot(degree_shift=5),
    Slot(degree_shift=2),
    Slot(degree_shift=4),
    Slot(degree_shift=5),
    Slot(),
])

# play the second note of a triad or pattern one note up, the second two notes up
api.transforms.add(name='octave ramp', slots=[
    Slot(),
    Slot(octave_shift=1),
    Slot(octave_shift=2)
])

# quickly repeat the notes with alternating silence, the last repeat is only randomly silent
api.transforms.add(name='stutter', divide=6, applies_to='notes', slots=[
    Slot(),
    Slot(rest=True),
    Slot(),
    Slot(rest=True),
    Slot(),
    Slot(rest=Probability(0.5, True, False))
])

# turn whatever is playing into chords, or change the active chord type
# divide=1 means don't arpeggiate
api.transforms.add(name='chordify', applies_to='notes', divide=1, slots=[
    Slot(chord_type='major'),
    Slot(chord_type='minor')
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
api.scenes.add(name='scene_11', rate=0.5, auto_advance=True)
api.scenes.add(name='scene_END', rate=0.5, auto_advance=True)

# ======================================================================================================================
# setup clips

api.clips.add(name='chord strum', scene='scene_1', track='lead', scales=['C-major'],
              patterns=['chords'], transforms=['basic arp'], repeat=2, auto_scene_advance=True)

api.clips.add(name='chord octave arp', scene='scene_2', track='lead', scales=['C-major'],
              patterns=['chords'], transforms=['octave arp'], repeat=2, auto_scene_advance=True)

api.clips.add(name='chord velocity', scene='scene_3', track='lead', scales=['C-major'],
              patterns=['chords'], transforms=['velocity arp'], repeat=1, auto_scene_advance=True)

api.clips.add(name='chord ccs', scene='scene_4', track='lead', scales=['C-major'],
              patterns=['chords'], transforms=['midi cc arp'], repeat=1, auto_scene_advance=True)

api.clips.add(name='melody to bassline', scene='scene_5', track='lead', scales=['C-major'],
              patterns=['basic'], transforms=['bassline'], repeat=1, auto_scene_advance=True)

# explaining multiple transforms:
#
# the list of transforms applies to each pattern that plays in turn. Yet each step in the list can contain one or
# more transforms if more than one is supplied, the 2nd and later transforms apply to the results of the first

api.clips.add(name='melody octave adjustment, then stutter', scene='scene_6', track='lead', scales=['C-major'],
              patterns=['basic'], transforms=['octave ramp', 'stutter'], repeat=2, auto_scene_advance=True)

api.clips.add(name='stacked transforms', scene='scene_7', track='lead', scales=['C-major'],
              patterns=['basic'], transforms=[['octave ramp','stutter'],'bassline',['octave arp','basic arp']],
              repeat=3,  auto_scene_advance=True)

api.clips.add(name='just arp the chords', scene='scene_8', track='lead', scales=['C-major'],
              patterns=['chords','basic'], transforms=['basic arp'], repeat=1,  auto_scene_advance=True)

api.clips.add(name='just tweak the notes', scene='scene_9', track='lead', scales=['C-major'],
              patterns=['chords','basic'], transforms=['stutter'], repeat=1,  auto_scene_advance=True)

api.clips.add(name='transform melody to chords then arp', scene='scene_10', track='lead', scales=['C-major'],
              patterns=['basic'], transforms=[['chordify','basic arp']], repeat=1, auto_scene_advance=True)

api.clips.add(name='chord octave shift', scene='scene_11', track='lead', scales=['C-major'],
              patterns=['chords'], transforms=['octave up'], repeat=1, auto_scene_advance=True)

# ======================================================================================================================
# play starting on the first scene - Ctrl+C to exit.

api.player.loop('scene_1')
