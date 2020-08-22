# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

from wsgiref import simple_server
import falcon
from warpseq.server.mailbox import Mailbox, Message

class BaseResource(object):

    __slots__ = ('mailbox',)

    def __init__(self, mailbox=None):

        self.mailbox = mailbox

class ThingsResource(BaseResource):

    __slots__ = ()

    def on_get(self, req, resp):


        resp.status = falcon.HTTP_200  # This is the default status

        reply = self.mailbox.send_message_and_wait_for_reply(Message('whazzup'))
        print("GOT RESPONSE: %s" % reply.body)

        resp.body = reply.body

        return resp



def run_server(host='127.0.0.1', port=8000, to_engine=None, to_server=None):

    mailbox = Mailbox(receive_queue=to_server, send_queue=to_engine)

    app = falcon.API()
    app.add_route('/things', ThingsResource(mailbox=mailbox))

    httpd = simple_server.make_server(host, port, app)
    httpd.serve_forever()

