# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

import json

class SongApi(object):

    def __init__(self, public_api, song):
        self.public_api = public_api
        self.song = song

    def edit(self, tempo:int=None, scale:str=None):
        if tempo:
            self.song.tempo = tempo
        if scale:
            scale = self.public_api.scales.lookup(scale, require=True)
            self.song.scale = scale

    def to_dict(self):
        return self.song.to_dict()

    def to_json(self):
        return json.dumps(self.to_dict(), sort_keys=True, indent=4)