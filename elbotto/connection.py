
import json
import logging

import websocket

from elbotto import messages

logger = logging.getLogger(__name__)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")


class Connection(object):

    def __init__(self, server_address, bot):
        self.server_address = server_address
        self.bot = bot

    def on_message(self, ws, event):
        logger.debug("Received message %s", event)
        payload = json.loads(event)
        type = payload["type"]
        try:
            payload_data = payload["data"]
        except KeyError:
            payload_data = {}
        incoming = messages.create(type, payload_data)
        self.bot.handle_message(incoming)

    @staticmethod
    def create(server_address, bot):
        connection = Connection(server_address, bot)
        bot.connection = connection
        connection.connect()
        return connection

    def send(self, message):
        payload = json.dumps(message)
        logger.debug("Sending message %s", payload)
        self.ws.send(payload)

    def connect(self):
        logger.debug("Connecting to %s", self.server_address)
        # websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp(self.server_address,
                                    on_message=self.on_message,
                                    on_error=on_error,
                                    on_close=on_close)
        self.ws.run_forever()