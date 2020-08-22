# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

from warpseq.server.engine import run_engine as server_run_engine

def run_engine(to_engine=None, to_server=None):
    server_run_engine(to_engine=to_engine, to_server=to_server)

