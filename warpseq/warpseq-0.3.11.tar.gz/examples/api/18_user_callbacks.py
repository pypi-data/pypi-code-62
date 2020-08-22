# --------------------------------------------------------------
# Warp API Demo
# (C) Michael DeHaan <michael@michaeldehaan.net>, 2020
# --------------------------------------------------------------
#
# this demo shows how to use user callbacks to hook
# all the lifecycle events in Warp
# it is based on 01_scales.py

from warpseq.api import demo
from warpseq.api.public import Api as WarpApi
from warpseq.model.slot import Slot
from warpseq.api.callbacks import BaseCallbacks

# ======================================================================================================================

class UserCallbacks(BaseCallbacks):

    # WARNING: while most of the API is fairly stable, the callbacks API may be subject to slight changes in the
    # near future as the UI is developed and we see what data it requires.
    # Consult BaseCallbacks for the latest signature

    __slots__ = ()

    def on_init(self):
        pass

    def _announce(self, category, msg):
        print("message from UserCallbacks >>>> (%s) | %s" % (category, msg))

    def on_scene_start(self, scene):
        self._announce("scene_start", scene.name)

    def on_clip_start(self, clip):
        self._announce("clip_start", clip.name)

    def on_clip_stop(self, clip):
        self._announce("clip_stop", clip.name)

    def on_clip_restart(self, clip):
        self._announce("clip_restart", clip.name)

    def on_pattern_start(self, clip, pattern):
        self._announce("pattern_start", "%s/%s" % (clip.name, pattern.name))

    def all_clips_done(self):
        self._announce("all_clips_done", "!")

    def keyboard_interrupt(self):
        self._announce("keyboard_interrupt", "!!")


# ======================================================================================================================
# setup API and song

api = WarpApi()
api.remove_callbacks()
api.add_callbacks(UserCallbacks())
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
api.scales.add(name='C-minor', note='C', octave=0, scale_type='natural_minor')
api.scales.add(name='G-major', note='G', octave=0, scale_type='major')
api.scales.add(name='G-minor', note='G', octave=0, scale_type='natural_minor')
api.scales.add(name='Bb-mixolydian', note='Bb', octave=0, scale_type='mixolydian')
api.scales.add(name='A-akebono', note='A', octave=0, scale_type='akebono')
api.scales.add(name='F-user1', note='F', octave=0, slots = [1, 'b2', 'b3', '5', 6 ])
api.scales.add(name='F-user2', note='F', octave=1, slots = [1, 'b2', 'b3', '5', 6 ])

# ======================================================================================================================
# setup patterns

seq1 = [ Slot(degree=i) for i in [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16] ]
seq2 = [ Slot(degree=i) for i in [8,7,6,5,4,3,2,1] ]

api.patterns.add(name='up', slots=seq1)
api.patterns.add(name='down', slots=seq2)

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

# ======================================================================================================================
# setup clips

api.clips.add(name='C major up', scene='scene_1', track='lead', scales=['C-major'], patterns=['up'], repeat=1, auto_scene_advance=True)
api.clips.add(name='C minor up', scene='scene_2', track='lead', scales=['C-minor'], patterns=['up'], repeat=1, auto_scene_advance=True)
api.clips.add(name='G major up', scene='scene_3', track='lead', scales=['G-major'], patterns=['up'], repeat=1, auto_scene_advance=True)
api.clips.add(name='G minor up', scene='scene_4', track='lead', scales=['G-minor'], patterns=['up'], repeat=1, auto_scene_advance=True)
api.clips.add(name='Bb mixolydian up', scene='scene_5', track='lead', scales=['Bb-mixolydian'], patterns=['up'], repeat=1, auto_scene_advance=True)
api.clips.add(name='A akebono up', scene='scene_6', track='lead', scales=['A-akebono'], patterns=['up'], repeat=1, auto_scene_advance=True)
api.clips.add(name='Many scales down', scene='scene_7', track='lead', scales=['C-major','G-minor','A-akebono'], patterns=['down'], repeat=3, auto_scene_advance=True)
api.clips.add(name='Two user scales, also down', scene='scene_8', track='lead', scales=['F-user1', 'F-user2'], patterns=['down'], repeat=2, auto_scene_advance=True)

# ======================================================================================================================
# play starting on the first scene - Ctrl+C to exit.

api.player.loop('scene_1', infinite=True)
