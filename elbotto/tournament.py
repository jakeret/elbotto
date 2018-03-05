import logging
import threading

from elbotto.bots import stochastic, rlagent

DEFAULT_BOT_NAME = "El botto del jasso"

DEFAULT_SERVER_NAME = "ws://127.0.0.1:3000"

OUTPUT_PATH = "/Users/joak/workspace/jass/elbotto/dqnagent/"

def launch(bot_class, bot_name, server_address=DEFAULT_SERVER_NAME):
    bot_class(server_address, bot_name)


def create_bot_thread(kwargs):
    return threading.Thread(target=launch, kwargs=kwargs)


def start_bots():
    # create_bot_thread(dict(bot_class=rlagent.Bot,
    #                        bot_name="El botto del jasso 0",
    #                        output_path=OUTPUT_PATH + "bot0/",
    #                        save_episodes=100,
    #                        chosen_team_index=1)).start()
    #
    # create_bot_thread(dict(bot_class=rlagent.Bot,
    #                        bot_name="El botto del jasso 1",
    #                        output_path=OUTPUT_PATH + "bot1/",
    #                        save_episodes=None,
    #                        chosen_team_index=1)).start()

    create_bot_thread(dict(bot_class=stochastic.Bot,
                           bot_name="stochastic 0",
                           chosen_team_index=1)).start()

    t = create_bot_thread(dict(bot_class=stochastic.Bot,
                           bot_name="stochastic 1",
                           chosen_team_index=1))

    t.start()
    t.join()


if __name__ == '__main__':
    start_bots()