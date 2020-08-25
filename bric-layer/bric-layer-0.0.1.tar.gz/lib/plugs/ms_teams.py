import pymsteams


def send_message(message, webhook):
    pymsteams.connectorcard(webhook).text(message).send()


class MSTeamsAPI:
    def __init__(self, layer):
        self.layer = layer

        self.send_message = send_message
