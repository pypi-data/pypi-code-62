# --------------------------------------------------------------
# Warp API Demo
# (C) Michael DeHaan <michael@michaeldehaan.net>, 2020
# --------------------------------------------------------------
#
# this demo shows how to express basic chords using roman
# numerals and other chord types with mod expressions. Chords
# will pick up the assigned scale.
#
# it also shows how to use ties ("-") and how to mix chords
# and scale notes.

from warpseq.api import demo
from warpseq.api.public import Api as WarpApi
from warpseq.model.slot import Slot

# ======================================================================================================================
# setup API and song

api = WarpApi()
api.song.edit(tempo=100)

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

api.patterns.add(name='quiet', slots=[
    Slot(rest=True),
    Slot(rest=True)
])

api.patterns.add(name='major_hold', slots=[
    Slot(degree=1, chord_type='major'),
    Slot(tie=True),
    Slot(tie=True),
    Slot(tie=True),
    Slot(tie=True),
])

api.patterns.add(name='major_gap', slots=[
    Slot(degree=1, chord_type='major'),
    Slot(rest=True),
    Slot(rest=True),
    Slot(rest=True),
    Slot(rest=True),
    Slot(rest=True),
]
                 )
api.patterns.add(name='major_chords', slots=[
    Slot(degree=1, chord_type='major'),
    Slot(degree=4, chord_type='major'),
    Slot(degree=5, chord_type='major')
])

api.patterns.add(name='minor_chords', slots=[
    Slot(degree=2, chord_type='minor'),
    Slot(degree=3, chord_type='minor'),
    Slot(degree=6, chord_type='minor'),
])

api.patterns.add(name='inversions', slots=[
    Slot(degree=1, chord_type='major', inversion=1),
    Slot(degree=1, chord_type='major', inversion=2),
    Slot(degree=1, chord_type='M6', inversion=3)
])

api.patterns.add(name='chords_with_silence_and_then_notes', slots = [
    Slot(degree=1, chord_type='major'),
    Slot(rest=True),
    Slot(degree=2),
    Slot(degree=3),
    Slot(degree=4),
    Slot(degree=5),
    Slot(degree=6),
    Slot(degree=7),
])

api.patterns.add(name='chords_with_ties_and_notes', slots = [
    Slot(degree=1, chord_type='major'),
    Slot(tie=True),
    Slot(degree=1),
    Slot(degree=2),
    Slot(degree=3),
    Slot(degree=4),
])

api.patterns.add(name='all_chord_types', slots = [
    Slot(degree=1, chord_type='major'),
    Slot(degree=2, chord_type='minor'),
    Slot(degree=3, chord_type='dim'),
    Slot(degree=4, chord_type='aug'),
    Slot(degree=5, chord_type='sus4'),
    Slot(degree=6, chord_type='sus2'),
    Slot(degree=7, chord_type='fourth'),
    Slot(degree=1, chord_type='fifth'),
    Slot(degree=2, chord_type='M6'),
    Slot(degree=3, chord_type='m6'),
    Slot(degree=4, chord_type='dom7'),
    Slot(degree=5, chord_type='aug7'),
    Slot(degree=6, chord_type='dim7'),
    Slot(degree=7, chord_type='mM7')
])

# ======================================================================================================================
# setup scenes

api.scenes.add(name='scene_0', rate=0.5, auto_advance=True)
api.scenes.add(name='scene_1', rate=0.5, auto_advance=True)
api.scenes.add(name='scene_2', rate=0.5, auto_advance=True)
api.scenes.add(name='scene_3', rate=0.5, auto_advance=True)
api.scenes.add(name='scene_4', rate=0.5, auto_advance=True)
api.scenes.add(name='scene_5', rate=0.5, auto_advance=True)
api.scenes.add(name='scene_6', rate=0.5, auto_advance=True)

# ======================================================================================================================
# setup clips

api.clips.add(name='major chords with ties', scene='scene_0', track='lead', scales=['C-major'], patterns=['major_hold', 'quiet'], repeat=1, auto_scene_advance=True)
api.clips.add(name='major chords with rests', scene='scene_1', track='lead', scales=['C-major'], patterns=['major_chords','quiet'], repeat=1, auto_scene_advance=True)
api.clips.add(name='minor chords', scene='scene_2', track='lead', scales=['C-major'], patterns=['minor_chords','quiet'], repeat=1, auto_scene_advance=True)
api.clips.add(name='chords with rests and notes', scene='scene_3', track='lead', scales=['C-major'], patterns=['chords_with_silence_and_then_notes','quiet'], repeat=1, auto_scene_advance=True)
api.clips.add(name='chords with ties and notes', scene='scene_4', track='lead', scales=['C-major'], patterns=['chords_with_ties_and_notes','quiet'], repeat=1, auto_scene_advance=True)
api.clips.add(name='chord types menu assortment', scene='scene_5', track='lead', scales=['C-major'], patterns=['all_chord_types','quiet'], repeat=1, auto_scene_advance=True)
api.clips.add(name='chord inversions', scene='scene_6', track='lead', scales=['C-major'], patterns=['inversions', 'quiet'], repeat=1, auto_scene_advance=True)

# ======================================================================================================================
# play starting on the first scene - Ctrl+C to exit.

api.player.loop('scene_0')
