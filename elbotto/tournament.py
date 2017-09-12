import threading

from elbotto import launcher
from elbotto.strategy import stochastic

DEFAULT_BOT_NAME = "El botto del jasso"

DEFAULT_SERVER_NAME = "ws://127.0.0.1:3000"


def launch(bot_class, bot_name, server_address=DEFAULT_SERVER_NAME):
    bot_class(server_address, bot_name)

def start_bots():
    threading.Thread(target=launch, kwargs={"bot_class": stochastic.Bot, "bot_name": DEFAULT_BOT_NAME}).start()
    threading.Thread(target=launch, kwargs={"bot_class": stochastic.Bot, "bot_name": DEFAULT_BOT_NAME}).start()
    threading.Thread(target=launch, kwargs={"bot_class": stochastic.Bot, "bot_name": "Dude"}).start()
    t = threading.Thread(target=launch, kwargs={"bot_class": stochastic.Bot, "bot_name": "Dude"})

    t.start()
    t.join()


if __name__ == '__main__':
    start_bots()