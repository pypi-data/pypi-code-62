# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

from warpseq.server.mailbox import Mailbox, Message
import time

def run_engine(to_engine=None, to_server=None):

    mailbox = Mailbox(receive_queue=to_engine, send_queue=to_server)

    while True:

        try:

            messages = mailbox.get_unexpected_messages()

            for msg in messages:
                if msg.body == 'whazzup':
                    mailbox.send_reply(msg, Message(body='howz it going'))

        except KeyboardInterrupt:

            return

        time.sleep(0.1)