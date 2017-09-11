import logging

from elbotto.bot import Bot
from elbotto.connection import Connection
from elbotto.strategy.stochastic import PlayStrategy

logging.basicConfig(level=logging.INFO)

DEFAULT_BOT_NAME = "El botto del jasso"

DEFAULT_SERVER_NAME = "ws://127.0.0.1:3000"


def launch(bot_name=DEFAULT_BOT_NAME, server_address=DEFAULT_SERVER_NAME):
    game_strategy = PlayStrategy()
    bot = Bot(bot_name, game_strategy)
    connection = Connection.create(server_address, bot)

if __name__ == '__main__':
    launch()