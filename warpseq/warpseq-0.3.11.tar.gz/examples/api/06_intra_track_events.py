# --------------------------------------------------------------
# Warp API Demo
# (C) Michael DeHaan <michael@michaeldehaan.net>, 2020
# --------------------------------------------------------------
#
# this demos hows how instruments can pull notes selectively
# from a silent guide track, which can be useful to rapidly
# construct large movements without having to sequence notes
# for every single instrument.
#
# Basically one instrument can "listen" to what is playing on another track, copy the note,
# and then use it to build chords, transpose up or down, or apply an arpeggiator.

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

api.instruments.add('guide', device=DEVICE, channel=4, min_octave=0, base_octave=4, max_octave=10, muted=True)
api.instruments.add('lead_inst', device=DEVICE, channel=1, min_octave=0, base_octave=4, max_octave=10, muted=False)
api.instruments.add('bass_inst', device=DEVICE, channel=2, min_octave=0, base_octave=4, max_octave=10,muted=False)

# ======================================================================================================================
# setup tracks

api.tracks.add(name='guide', instrument='guide')
api.tracks.add(name='lead', instrument='lead_inst')
api.tracks.add(name='bass', instrument='bass_inst')

# ======================================================================================================================
# setup scales

api.scales.add(name='Eb-lydian', note='Eb', octave=0, scale_type='lydian')
api.scales.add(name='B-minor', note='B', octave=0, scale_type='natural_minor')

# ======================================================================================================================
# setup patterns

api.patterns.add(name='a', slots=[
    Slot(degree=1),
    Slot(degree=2),
    Slot(degree=3),
    Slot(degree=4),
    Slot(degree=5),
    Slot(degree=6),
    Slot(degree=7),
])

api.patterns.add(name='b', slots = [
    Slot(degree=7),
    Slot(degree=6),
    Slot(degree=5),
    Slot(degree=4),
    Slot(degree=3),
    Slot(degree=2),
    Slot(degree=1),

])

api.patterns.add(name='parrot', slots = [
    Slot(track_grab='guide')
])

api.patterns.add(name='stylish parrot', slots = [
    Slot(track_grab='guide', chord_type='major', octave_shift=1),
    Slot(track_grab='guide'),
    Slot(track_grab='guide'),
    Slot(track_grab='guide'),
])

api.patterns.add(name='even', slots = [
    Slot(track_grab='guide'),
    Slot(rest=True),
    Slot(track_grab='guide'),
    Slot(rest=True),
    Slot(degree=5),
    Slot(rest=True),
])

api.patterns.add(name='odd', slots = [
    Slot(rest=True),
    Slot(track_grab='guide'),
    Slot(rest=True),
    Slot(track_grab='guide'),
    Slot(rest=True),
    Slot(degree=5)
])

api.patterns.add(name='chords', slots = [
    Slot(track_grab='guide', chord_type='major'),
    Slot(tie=True),
    Slot(tie=True),
    Slot(rest=True),
])

# ======================================================================================================================
# setup transforms

api.transforms.add(name='bassline', divide=8, slots=[
    Slot(),
    Slot(degree_shift=1),
    Slot(degree_shift=4),
    Slot(degree_shift=5)
])

api.transforms.add(name='octave_down', divide=1, slots=[
    Slot(octave_shift=-1)
])

api.transforms.add(name='grab', divide=1, slots=[
    Slot(octave_shift=-1)
])

# ======================================================================================================================
# setup scenes

api.scenes.add(name='scene_1', rate=1, auto_advance=True, scale='Eb-lydian')
api.scenes.add(name='scene_2', rate=1, auto_advance=True, scale='B-minor')
api.scenes.add(name='scene_3', rate=1, auto_advance=True, scale='B-minor')
api.scenes.add(name='scene_4', rate=1, auto_advance=True, scale='B-minor')
api.scenes.add(name='scene_5', rate=1, auto_advance=True, scale='Eb-lydian')

# ======================================================================================================================
# setup clips

# at start, the lead just plays whatever the guide track is silently playing

api.clips.add(name='s1_guide', scene='scene_1', track='guide', patterns=['a','b','a','b'],
              repeat=1, auto_scene_advance=True)

api.clips.add(name='s1_lead', scene='scene_1', track='lead', patterns=['parrot'],
              repeat=None) # repeat=None means infinite

# now the bass track plays the guide track instead of the lead

api.clips.add(name='s2_guide', scene='scene_2', track='guide', patterns=['a','b','a','b'],
              repeat=1, auto_scene_advance=True)

api.clips.add(name='s2_bass', scene='scene_2', track='bass', patterns=['parrot'], repeat=None)

# now the lead and bass track alternate notes from the guide track and some things they have decided for themselves.
# not all slots have to grab the value from the guide track

api.clips.add(name='s3_guide', scene='scene_3', track='guide', patterns=['a','b','a','b'],
              repeat=1, auto_scene_advance=True)

api.clips.add(name='s3_bass', scene='scene_3', track='lead', patterns=['even'],
              repeat=None) # repeat=None means infinite

api.clips.add(name='s3_lead', scene='scene_3', track='bass', patterns=['odd'], repeat=None)

# now the lead track slowly plays a chord based on the silent guide track while the bass track forms a
# bassline around it.

api.clips.add(name='s4_guide', scene='scene_4', track='guide', patterns=['a','b','a','b'],
              repeat=1, auto_scene_advance=True)

api.clips.add(name='s4_bass', scene='scene_4', track='lead', patterns=['chords'], rate=0.5,
              repeat=None) # repeat=None means infinite

api.clips.add(name='s4_lead', scene='scene_4', track='bass', patterns=['parrot'], rate=1,
              transforms=[['octave_down','bassline']], repeat=None)

# ======================================================================================================================
# play starting on the first scene - Ctrl+C to exit.

api.player.loop('scene_4')
