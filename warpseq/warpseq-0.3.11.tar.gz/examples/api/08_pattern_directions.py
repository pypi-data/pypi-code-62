# --------------------------------------------------------------
# Warp API Demo
# (C) Michael DeHaan <michael@michaeldehaan.net>, 2020
# --------------------------------------------------------------
#
# shows how pattern directions work.

from warpseq.api import demo
from warpseq.api.public import Api as WarpApi
from warpseq.model.slot import Slot

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

seq = [
    Slot(degree=1),
    Slot(degree=2),
    Slot(degree=3),
    Slot(degree=4),
    Slot(degree=5),
    Slot(degree=6),
    Slot(degree=7),
]

seq2 =[
    Slot(degree=1),
    Slot(degree=2),
    Slot(degree=3)
]

seq3 = [
    Slot(degree=1),
    Slot(degree=2),
    Slot(degree=3),
    Slot(degree=4)
]

# ======================================================================================================================
# setup patterns

api.patterns.add(name='up1', slots=seq, direction='forward')
api.patterns.add(name='down1', slots=seq, direction='reverse')
api.patterns.add(name='oscillate1', slots=seq, direction='oscillate')
api.patterns.add(name='pendulum1', slots=seq, direction='pendulum')
api.patterns.add(name='serialized1', slots=seq, direction='serialized', rate=0.5)
api.patterns.add(name='random1', slots=seq, direction='random', rate=0.5)
api.patterns.add(name='brownian1', slots=seq, direction='brownian1', rate=1)
api.patterns.add(name='brownian2', slots=seq, direction='brownian2', rate=1)
api.patterns.add(name='brownian3', slots=seq, direction='brownian3', rate=1)
api.patterns.add(name='brownian4', slots=seq, direction='brownian4', rate=1)
api.patterns.add(name='brownian5', slots=seq, direction='brownian5', rate=1)
api.patterns.add(name='brownian6', slots=seq, direction='brownian6', rate=1)
api.patterns.add(name='up2', slots=seq2, direction='forward', length=10)
api.patterns.add(name='up3', slots=seq3, direction='forward', length=10)
api.patterns.add(name='build1', slots=seq, length=10, direction='build')

# ======================================================================================================================
# setup scenes

api.scenes.add(name='scene_1', rate=1, auto_advance=True)
api.scenes.add(name='scene_2', rate=1, auto_advance=True)
api.scenes.add(name='scene_3', rate=1, auto_advance=True)
api.scenes.add(name='scene_4', rate=1, auto_advance=True)
api.scenes.add(name='scene_5', rate=1, auto_advance=True)
api.scenes.add(name='scene_6', rate=1, auto_advance=True)
api.scenes.add(name='scene_7', rate=1, auto_advance=True)
api.scenes.add(name='scene_8', rate=1, auto_advance=True)
api.scenes.add(name='scene_9', rate=1, auto_advance=True)
api.scenes.add(name='scene_10', rate=1, auto_advance=True)
api.scenes.add(name='scene_11', rate=1, auto_advance=True)
api.scenes.add(name='scene_12', rate=1, auto_advance=True)
api.scenes.add(name='scene_13', rate=1, auto_advance=True)
api.scenes.add(name='scene_14', rate=1, auto_advance=True)
api.scenes.add(name='scene_END', rate=1, auto_advance=True)

# ======================================================================================================================

# setup clips
api.clips.add(name='forward and reverse patterns', scene='scene_1', track='lead', scales=['C-major'], patterns=['up1','down1','up1','down1'], repeat=1, auto_scene_advance=True)
api.clips.add(name='oscillating patterns', scene='scene_2', track='lead', scales=['F-pentatonic-minor'], patterns=['oscillate1'], repeat=4, auto_scene_advance=True)
api.clips.add(name='pendulum patterns', scene='scene_3', track='lead', scales=['C-major'], patterns=['pendulum1'], repeat=4, auto_scene_advance=True)
api.clips.add(name='serialized patterns', scene='scene_4', track='lead', scales=['C-major'], patterns=['serialized1'], repeat=4, auto_scene_advance=True)
api.clips.add(name='random patterns', scene='scene_5', track='lead', scales=['C-major'], patterns=['random1'], repeat=4, auto_scene_advance=True)
api.clips.add(name='brownian1', scene='scene_6', track='lead', scales=['C-major'], patterns=['brownian1'], repeat=4, auto_scene_advance=True)
api.clips.add(name='brownian2', scene='scene_7', track='lead', scales=['C-major'], patterns=['brownian2'], repeat=4, auto_scene_advance=True)
api.clips.add(name='brownian3', scene='scene_8', track='lead', scales=['C-major'], patterns=['brownian3'], repeat=4, auto_scene_advance=True)
api.clips.add(name='brownian4', scene='scene_9', track='lead', scales=['C-major'], patterns=['brownian4'], repeat=4, auto_scene_advance=True)
api.clips.add(name='brownian5', scene='scene_10', track='lead', scales=['C-major'], patterns=['brownian5'], repeat=4, auto_scene_advance=True)
api.clips.add(name='brownian6', scene='scene_11', track='lead', scales=['C-major'], patterns=['brownian6'], repeat=4, auto_scene_advance=True)
api.clips.add(name='forward with extra length', scene='scene_12', track='lead', scales=['C-major'], patterns=['up2'], repeat=4, auto_scene_advance=True)
api.clips.add(name='forward with shortened length', scene='scene_13', track='lead', scales=['C-major'], patterns=['up3'], repeat=4, auto_scene_advance=True)
api.clips.add(name='build and stick', scene='scene_13', track='lead', scales=['C-major'], patterns=['build1'], repeat=4, auto_scene_advance=True)

# ======================================================================================================================
# play starting on the first scene - Ctrl+C to exit.

api.player.loop('scene_1')