import os
import logging
from collections import Counter

import tensorflow as tf
from tensorforce import Configuration
from tensorforce.agents import DQNAgent
from tensorforce.core.networks import layered_network_builder

import numpy as np

from elbotto.basebot import BaseBot, DEFAULT_TRUMPF
from elbotto.card import Card, Color, CARD_OFFSET, CARDS_PER_COLOR
from elbotto.messages import GameType

logger = logging.getLogger(__name__)


def create_training_path(base_path):
    idx = 0
    path = os.path.join(base_path, "run_{:03d}".format(idx))
    while os.path.exists(path):
        idx += 1
        path = os.path.join(base_path, "run_{:03d}".format(idx))
    return path


REJECT_CARD_REWARD = -1

INVALID_CARD_REWARD = REJECT_CARD_REWARD

MAX_STICH = 9

MAX_STICH_POINTS = 256

states = dict(shape=(8 * (CARDS_PER_COLOR + 1)), type='float')

actions=dict(continuous=False, num_actions=36)

def load_network():
    layers = [
        # dict(type='dense', size=64),
        dict(type='dense', size=128),
        dict(type='dense', size=128),
        dict(type='lstm'),
    ]
    network = layered_network_builder(layers_config=layers)
    return network


def load_dqn_config(summary_output_path):
    config = Configuration(
        states = states,
        actions = actions,
        network = load_network(),

        preprocessing=None,
        exploration= dict(
            type= "epsilon_decay",
            epsilon= 1.0,
            epsilon_final= 0.1,
            epsilon_timesteps= 1e6
        ),
        reward_preprocessing=#None,
        [
            dict(
                type= "clip",
                min= -1,
                max= 1
            )
        ],
        batch_size= 32,
        memory_capacity= 10000,
        memory= dict(
            type= "replay",
            random_sampling= False
        ),
        update_frequency= 4,
        first_update= 50000,
        repeat_update= 1,

        target_update_frequency= 10000,

        discount= 0.99,
        learning_rate= 0.00025,
        optimizer= dict(
            type= "rmsprop",
            momentum= 0.95,
            epsilon= 0.01
        ),
        tf_saver= True,
        tf_summary=summary_output_path,
        tf_summary_level=3,
        log_level= "info",

        update_target_weight= 1.0,
        double_dqn= True,
        clip_loss= 0.0
    )
    return config


def load_agent(summary_output_path):
    config = load_dqn_config(summary_output_path)
    agent = DQNAgent(config=config)
    return agent


class Bot(BaseBot):

    def __init__(self, server_address, name, output_path, training=True, save_episodes=None, chosen_team_index=0):
        super(Bot, self).__init__(server_address, name, chosen_team_index)

        output_path = create_training_path(output_path)

        self.model_save_path = os.path.join(output_path, "model")
        self.save_episodes = save_episodes
        self.training = training
        self.episode = 1
        self.episode_reward = 0
        self.stich_number = 0

        self.played_cards_in_game = []

        logger.info("Summay output path %s", output_path)

        self.agent = load_agent(output_path)

        if not self.training:
            self.agent.load_model(output_path)

        self.winning_rate_node = tf.placeholder(tf.float32, name='winning-rate-placeholder')
        self.winning_rate_summary = tf.summary.scalar('winning-rate', self.winning_rate_node)

        self.start()

    def handle_request_trumpf(self):
        cnt = Counter()
        for card in self.handCards:
            cnt[card.color] += 1
        most_common_color = cnt.most_common(1)[0][0]
        return GameType("TRUMPF", most_common_color.name)

    def handle_played_cards(self, played_cards):
        super(Bot, self).handle_played_cards(played_cards)

        for card in played_cards:
            if card not in self.played_cards_in_game:
                self.played_cards_in_game.append(card)

    def handle_stich(self, winner, round_points, total_points):
        self.stich_number += 1
        won_stich = self.in_my_team(winner)
        # logger.info("%s: %s, %s, %s", self.episode, self.name, winner, won_stich)
        reward = round_points / MAX_STICH_POINTS
        self.episode_reward += reward

        logger.debug("Stich: Won:%s, Winner: %s, Round points: %s, episode_reward: %s", won_stich, winner.name, round_points, self.episode_reward)

        if self.training:
            self.agent.observe(reward=reward, terminal=self.stich_number==MAX_STICH)

    def handle_reject_card(self, card):
        # logger.warning(" ######   SERVER REJECTED CARD   #######")

        reward = REJECT_CARD_REWARD

        if self.training:
            self.agent.observe(reward=reward, terminal=False)

        self.episode_reward += reward

    def handle_request_card(self, tableCards):
        state = self._build_state()
        action = self.agent.act(state=state, deterministic = not self.training)
        card = self._convert_action_to_card(action)

        while card is None:
            if self.training:
                self.agent.observe(reward=INVALID_CARD_REWARD, terminal=False)

            action = self.agent.act(state=state, deterministic = not self.training)
            card = self._convert_action_to_card(action)

        return card

    def handle_game_finished(self):
        if self.model_save_path and self.save_episodes is not None and self.episode % self.save_episodes == 0:
            logger.info("Saving agent after episode {}".format(self.episode))
            logger.info("Model saved to: %s", self.model_save_path)
            self.agent.save_model(self.model_save_path)

        winning_rate = sum(self.won_stich_in_game) / len(self.won_stich_in_game)

        session = self.agent.model.session
        winning_rate_summary = session.run(self.winning_rate_summary,
                                          feed_dict={self.winning_rate_node: winning_rate})
        self.agent.model.writer.add_summary(winning_rate_summary, global_step=self.episode)


        logger.info("Episode %s, stich %s/%s, episode reward: %s"%(
            self.episode,
            sum(self.won_stich_in_game),
            len(self.won_stich_in_game),
            self.episode_reward))

        self.agent.observe_episode_reward(self.episode_reward)
        self.episode += 1
        self.episode_reward = 0
        self.stich_number = 0
        self.played_cards_in_game = []

    def _convert_action_to_card(self, action):
        card = Card.form_idx(int(action))
        for hard_card in self.handCards:
            if card == hard_card:
                return card

        return None

    # def _build_state(self):
    #     order = {self.game_type.trumpf_color: 0}
    #     for color in Color:
    #         if color != self.game_type.trumpf_color:
    #             order[color] = len(order)
    #
    #     state = np.zeros((4, CARDS_PER_COLOR), dtype=np.float32)
    #     for card in self.played_cards_in_game:
    #         state[order[card.color], card.number - CARD_OFFSET] = 1.0
    #
    #     return state.flatten()

    def _build_state(self):
        order = {}
        for color in Color:
            order[color] = len(order)

        state = np.zeros((8, CARDS_PER_COLOR + 1), dtype=np.float32)

        state[order[self.game_type.trumpf_color], 0] = 1.0

        for card in self.played_cards_in_game:
            state[order[card.color], 1 + card.number - CARD_OFFSET] = 1.0

        for card in self.handCards:
            state[4 + order[card.color], 1 + card.number - CARD_OFFSET] = 1.0

        return state.flatten()

