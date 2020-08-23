"""!
@author atomicfruitcake

@date 2020

Example gnutty server implementation
"""

import os
from pathlib import Path

from srv.gnutty import Gnutty
from srv.responses.response import Response
from srv.responses.response_codes import ResponseCodes


def run_gnutty():
    server = Gnutty(port=8000)

    @server.get("/")
    def root(request):
        return Response(body="OK")

    @server.get("/favicon.ico")
    def favicon(request):
        return Response(
            body=open(
                os.path.join(
                    Path(os.path.dirname(__file__)).parent,
                    "favicon.ico"
                ),
                "rb",
            ).read()
        )

    @server.post("/test", auth="basic")
    def new(request):
        return Response(
            body=request.body,
            content_type="application/json",
        )

    @server.any()
    def not_found(request):
        return Response(
            code=ResponseCodes.NOT_FOUND.value,
            body="NOT FOUND",
            content_type="text/html",
        )

    server.serve()


if __name__ == "__main__":
    run_gnutty()
