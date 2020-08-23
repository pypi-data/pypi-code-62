"""!
@author atomicfruitcake

@date 2020

Gnutty Server
"""
import os
from pathlib import Path

from srv import constants
from srv.gnuttycore import GnuttyCore


class Gnutty(GnuttyCore):
    """
    Gnutty Server class
    """

    def __init__(self, host="0.0.0.0", port=constants.PORT, favicon=None):
        """
        Constructor method for gnutty server
        :param host: str - Network interface IP where server will run
        :param port: int - Port where the server can be accessed from
        :param favicon: str - Path to favicon.ico to be used
        """
        self.host = host
        self.port = port
        super(Gnutty, self).__init__(host=self.host, port=self.port)

        self.favicon = (
            os.path.join(Path(os.path.dirname(__file__)).parent, "favicon.ico")
            if not favicon
            else favicon
        )
