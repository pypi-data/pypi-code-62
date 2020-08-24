# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

from warpseq.server.packet import ResponsePacket
import traceback

HELLO = 'hello'
LOAD = 'load'
PLAY_SCENE = 'play_scene'

class Dispatcher(object):

    __slots__ = ('api',)

    def __init__(self, api):
        self.api = api

    def dispatch(self, pkt):

        try:

            if pkt.cmd == HELLO:
                return ResponsePacket(msg='whazzup!')

            elif pkt.cmd == LOAD:
                self.api.load(pkt.name)
                return ResponsePacket()

            elif pkt.cmd == PLAY_SCENE:
                self.api.player.loop(pkt.name)
                return ResponsePacket()


            return ResponsePacket(ok=False, msg='unknown command')

        except:

            traceback.print_exc()

            return ResponsePacket(ok=False, msg='kaboom')

