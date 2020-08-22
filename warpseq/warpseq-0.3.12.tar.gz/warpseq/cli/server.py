# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

from warpseq.server.server import run_server as server_run_server

def run_server(to_engine=None, to_server=None):
    server_run_server(to_engine=to_engine, to_server=to_server)