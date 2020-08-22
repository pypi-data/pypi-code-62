# --------------------------------------------------------------
# Warp API Demo
# (C) Michael DeHaan <michael@michaeldehaan.net>, 2020
# --------------------------------------------------------------

# sharing a melody among multiple tracks in an advanced example, using both "track_copy" to
# direct notes to particular tracks, and TrackGrab to pull them in. Adding a serialized
# direction to the transform in the second scene means the notes are played by different
# instrument orders when the pattern repeats.

from warpseq.api import demo
from warpseq.api.public import Api as WarpApi
from warpseq.model.slot import Slot

# ======================================================================================================================
# setup API and song

api = WarpApi()
api.song.edit(tempo=50)

# ======================================================================================================================
# setup instruments

DEVICE = demo.suggest_device(api, 'IAC Driver IAC Bus 1')

api.instruments.add('snow_white', device=DEVICE, channel=16, min_octave=0, base_octave=3, max_octave=10, muted=True)
api.instruments.add('doc', device=DEVICE, channel=1, min_octave=0, base_octave=3, max_octave=10, muted=False)
api.instruments.add('happy', device=DEVICE, channel=2, min_octave=0, base_octave=3, max_octave=10, muted=False)
api.instruments.add('sneezy', device=DEVICE, channel=3, min_octave=0, base_octave=3, max_octave=10, muted=False)
api.instruments.add('sleepy', device=DEVICE, channel=4, min_octave=0, base_octave=3, max_octave=10, muted=False)
api.instruments.add('bashful', device=DEVICE, channel=5, min_octave=0, base_octave=3, max_octave=10, muted=False)
api.instruments.add('grumpy', device=DEVICE, channel=6, min_octave=0, base_octave=3, max_octave=10, muted=False)
api.instruments.add('dopey', device=DEVICE, channel=7, min_octave=0, base_octave=3, max_octave=10, muted=False)

# ======================================================================================================================
# setup tracks

api.tracks.add(name='conductor', instrument='snow_white', muted=False)
api.tracks.add(name='doc', instrument='doc', muted=False)
api.tracks.add(name='happy', instrument='happy', muted=False)
api.tracks.add(name='sneezy', instrument='sneezy', muted=False)
api.tracks.add(name='sleepy', instrument='sleepy', muted=False)
api.tracks.add(name='bashful', instrument='bashful', muted=False)
api.tracks.add(name='grumpy', instrument='grumpy', muted=False)
api.tracks.add(name='dopey', instrument='dopey', muted=False)

# ======================================================================================================================
# setup scales

api.scales.add(name='C-major', note='C', octave=0, scale_type='major')

# ======================================================================================================================
# setup transforms

# these patterns say for every note to pull the name of a track from a list (data patterns below) to send the notes to
# the first one will be in a constant order sequence. the second is in a random but serialized order

dwarf_sends = [
    Slot(track_copy="doc"),
    Slot(track_copy="happy"),
    Slot(track_copy="sneezy"),
    Slot(track_copy="sleepy"),
    Slot(track_copy="bashful"),
    Slot(track_copy="grumpy"),
    Slot(track_copy="dopey")
]

api.transforms.add(name='hocketInOrder', slots=dwarf_sends, divide=1, direction='forward')
api.transforms.add(name='hocketRandomly', slots=dwarf_sends, divide=1, direction='serialized')

# ======================================================================================================================
# setup music patterns

seq1 = [
    Slot(degree=1),
    Slot(degree=2),
    Slot(degree=3),
    Slot(degree=4),
    Slot(degree=5),
    Slot(degree=6),
    Slot(degree=7)
]

api.patterns.add(name='melody1', slots=seq1, direction='forward')

api.patterns.add(name='melody2', slots=seq1, direction='pendulum')

api.patterns.add(name='listen', slots=[
    Slot(track_grab='conductor')
])

# ======================================================================================================================
# setup scenes

api.scenes.add(name='scene_1', auto_advance=True)
api.scenes.add(name='scene_2', auto_advance=True)
api.scenes.add(name='scene_END', auto_advance=True)

# ======================================================================================================================
# setup clips

# first scene: each dwarf plays one note of the melody in order

api.clips.add(name='s1b', scene='scene_1', track='conductor', scales=['C-major'], patterns=['melody1'],
              transforms=['hocketInOrder'], repeat=4, auto_scene_advance=True)

api.clips.add(name='s1c', scene='scene_1', track='doc', patterns=['listen'], repeat=None)
api.clips.add(name='s1d', scene='scene_1', track='happy', patterns=['listen'], repeat=None)
api.clips.add(name='s1e', scene='scene_1', track='sneezy', patterns=['listen'], repeat=None)
api.clips.add(name='s1f', scene='scene_1', track='sleepy', patterns=['listen'], repeat=None)
api.clips.add(name='s1g', scene='scene_1', track='bashful', patterns=['listen'], repeat=None)
api.clips.add(name='s1h', scene='scene_1', track='grumpy', patterns=['listen'], repeat=None)
api.clips.add(name='s1i', scene='scene_1', track='dopey', patterns=['listen'], repeat=None)

# second scene: a random dwarf is chosen to play each note, but because the pattern hocketPattern2
# is serialized, each dwarf is # guaranteed to get exactly one note each before the dwarfs repeat

api.clips.add(name='s2b', scene='scene_2', track='conductor', scales=['C-major'], patterns=['melody1'],
              transforms=['hocketRandomly'], repeat=4, auto_scene_advance=True)

api.clips.add(name='s2c', scene='scene_2', track='doc', patterns=['listen'], repeat=None)
api.clips.add(name='s2d', scene='scene_2', track='happy', patterns=['listen'], repeat=None)
api.clips.add(name='s2e', scene='scene_2', track='sneezy', patterns=['listen'], repeat=None)
api.clips.add(name='s2f', scene='scene_2', track='sleepy', patterns=['listen'], repeat=None)
api.clips.add(name='s2g', scene='scene_2', track='bashful', patterns=['listen'], repeat=None)
api.clips.add(name='s2h', scene='scene_2', track='grumpy', patterns=['listen'], repeat=None)
api.clips.add(name='s2i', scene='scene_2', track='dopey', patterns=['listen'], repeat=None)

# ======================================================================================================================
# play starting on the first scene - Ctrl+C to exit.

api.player.loop('scene_1')