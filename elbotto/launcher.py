import logging

from elbotto.bots import stochastic, rlagent

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',)

DEFAULT_BOT_NAME = "El botto del jasso"

DEFAULT_SERVER_NAME = "ws://127.0.0.1:3000"

MODEL_SAVE_PATH = "/Users/joak/workspace/jass/elbotto/dqnagent/"

def launch(bot_name=DEFAULT_BOT_NAME, server_address=DEFAULT_SERVER_NAME):
    bot = stochastic.Bot(server_address, bot_name)
    #bot = rlagent.Bot(server_address, bot_name, MODEL_SAVE_PATH, save_episodes=100)

if __name__ == '__main__':
    launch()