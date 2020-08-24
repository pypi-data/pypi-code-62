# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

from wsgiref import simple_server
import falcon
import os
import sys
import jinja2

from warpseq.server.mailbox import Mailbox, Message
from warpseq.server.packet import CommandPacket
from warpseq.api.public import Api as WarpApi

#=======================================================================================================================

class BaseResource(object):

    __slots__ = ('mailbox', 'dispatcher')

    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self, mailbox=None):

        self.mailbox = mailbox

    # ------------------------------------------------------------------------------------------------------------------

    def _send_to_engine(self, data):
        return self.mailbox.send_message_and_wait_for_reply(Message(data)).body

# ======================================================================================================================

class ThingsResource(BaseResource):

    __slots__ = ()

    # ------------------------------------------------------------------------------------------------------------------

    def on_post(self, req, resp):

        data = CommandPacket.from_dict(req.media).to_dict()
        resp.media = self._send_to_engine(data)

    # ------------------------------------------------------------------------------------------------------------------


    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200  # This is the default status
        resp.body = 'ok'

# ======================================================================================================================

class WidgetsResource(BaseResource):

    def on_get(self, req, resp, category, item):
        resp.status = falcon.HTTP_200  # This is the default status
        resp.body = 'category: %s, item: %s' % (category, item)

# ======================================================================================================================

def run_server(host='127.0.0.1', port=8000, to_engine=None, to_server=None):

    mailbox = Mailbox(receive_queue=to_server, send_queue=to_engine)

    app = falcon.API()
    app.add_route('/svc', ThingsResource(mailbox=mailbox))

    app.add_route('/widgets/{category}/{item}', WidgetsResource(mailbox=mailbox))


    p = os.path.abspath(sys.modules[WarpApi.__module__].__file__)
    p = os.path.dirname(os.path.dirname(p))
    p = os.path.join(p, 'static')

    print("ready at http://%s:%s/index.html" % (host, port))
    print("serving content from: %s" % p)

    app.add_static_route('/', p)

    httpd = simple_server.make_server(host, port, app)
    httpd.serve_forever()

