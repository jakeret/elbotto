import json
import logging

from elbotto import messages, card
from elbotto.connection import Connection
from elbotto.messages import MessageType, GameType

logger = logging.getLogger(__name__)


SESSION_TYPE_TOURNAMENT = "TOURNAMENT"
SESSION_TYPE_SINGLE_GAME = "SINGLE_GAME"

DEFAULT_TRUMPF = GameType("TRUMPF", card.HEARTS)

class BaseBot(object):

    connection = None

    def __init__(self, server_address, name):
        self.name = name
        self.session_name = name
        self.server_address = server_address
        self.teams = None
        self.handCards= []

    def start(self):
        Connection.create(self.server_address, self)

    def handle_message(self, message):
        answer = None

        message_type = message["type"]
        try:
            data = message["data"]
        except KeyError:
            data = {}

        if message_type == MessageType.REQUEST_PLAYER_NAME["name"]:
            #CHALLENGE2017: Respond with your BotName
            logger.info('MyName: ' + self.name)
            answer = messages.create(MessageType.CHOOSE_PLAYER_NAME["name"], self.name)
            
        elif message_type == MessageType.REQUEST_SESSION_CHOICE["name"]:
            answer = messages.create(MessageType.CHOOSE_SESSION["name"], "AUTOJOIN", self.session_name, SESSION_TYPE_SINGLE_GAME, False)
            logger.info('session choice answer: %s', answer)
            
        elif message_type == MessageType.DEAL_CARDS["name"]:
            #CHALLENGE2017: Getting cards from server... just put them to your handcards
            self.handCards = data

        elif message_type == MessageType.REQUEST_TRUMPF["name"]:
            game_type = self.handle_request_trumpf()
            answer = messages.create(MessageType.CHOOSE_TRUMPF["name"], game_type)
            
        elif message_type == MessageType.REQUEST_CARD["name"]:
            card = self.handle_request_card(data)
            answer = messages.create(MessageType.CHOOSE_CARD["name"], card)
            
        elif message_type == MessageType.PLAYED_CARDS["name"]:
            #CHALLENGE2017: This removes a handcard if the last played card on the table was one of yours.
            lastPlayedCard = data[-1]
            handCards = []
            for card in self.handCards:
                if card.number != lastPlayedCard.number or card.color != lastPlayedCard.color:
                    handCards.append(card)

            self.handCards = handCards
            # self.handCards = self.handCards.filter(function (card) {
            #     return (card.number !== lastPlayedCard.number || card.color !== lastPlayedCard.color)
            # })
            
        elif message_type == MessageType.REJECT_CARD["name"]:
            self.handle_reject_card(data)
            
        elif message_type == MessageType.BROADCAST_GAME_FINISHED["name"]:
            self.handle_game_finished()

        elif message_type == MessageType.BROADCAST_SESSION_JOINED["name"]:
            self.player = data["player"]
            self.players_in_session = data["playersInSession"]

        elif message_type == MessageType.BROADCAST_STICH["name"]:
            winner = data["winner"]
            won = self.won(winner)
            round_points = self.round_points(data["score"])
            total_points = self.total_points(data["score"])
            self.handle_stich(won, winner, round_points, total_points)

        elif message_type == MessageType.BROADCAST_TOURNAMENT_STARTED["name"]:
            #Do nothing with that :-)
            pass
        elif message_type == MessageType.BROADCAST_TOURNAMENT_RANKING_TABLE["name"]:
            #Do nothing with that :-)
            pass
        elif message_type == MessageType.BROADCAST_TEAMS["name"]:
            self.teams = data
            for team in self.teams:
                if team.is_member(self.player):
                    self.my_team = team

        elif message_type == MessageType.BROADCAST_TRUMPF["name"]:
            self.handle_trumpf(data)

        elif message_type == MessageType.BROADCAST_WINNER_TEAM["name"]:
            #Do nothing with that :-)
            pass
        else:
            logger.warning("Sorry, i cannot handle this message: " + json.dumps(message))

        if answer:
            self.connection.send(answer)

    def handle_request_trumpf(self):
        # CHALLENGE2017: Ask the brain which gameMode to choose
        return DEFAULT_TRUMPF

    def handle_trumpf(self, game_type):
        self.geschoben = game_type.mode == "SCHIEBE"  # just remember if it's a geschoben match
        self.game_type = game_type

    def handle_stich(self, won, winner, round_points, total_points):
        # Do nothing with that :-)
        pass

    def handle_game_finished(self):
        # Do nothing with that :-)
        pass

    def handle_reject_card(self, data):
        # CHALLENGE2017: When server sends this, you send an invalid card... this should never happen!
        # Server will send "REQUEST_CARD" after this once. Make sure you choose a valid card or your bot will loose the game
        logger.warning(" ######   SERVER REJECTED CARD   #######")
        logger.warning("Rejected card: %s", data)
        logger.warning("Hand Cards: %s", self.handCards)
        logger.warning("Gametype: %s", self.game_type)

    def handle_request_card(self, tableCards):
        # CHALLENGE2017: Ask the brain which card to choose
        card = self.handCards[0]
        return card

    def won(self, winner):
        return self.player == winner

    def round_points(self, scores):
        for score in scores:
            if self.my_team.name == score.team_name:
                return score.current_round_points

        return 0

    def total_points(self, scores):
        for score in scores:
            if self.my_team.name == score.team_name:
                return score.points

        return 0