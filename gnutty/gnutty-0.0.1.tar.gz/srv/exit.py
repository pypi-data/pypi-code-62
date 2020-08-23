"""!
@author atomicfruitcake

@date 2020

Exit handler for gracefully shutting down the server
"""

import atexit
from srv.gnuttycore import GnuttyCore

def exit_handler():
    print("Deregistering sockets")
    GnuttyCore().sock.shutdown()

atexit.register(exit_handler)
