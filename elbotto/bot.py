import json
import logging

from elbotto import messages
from elbotto.messages import MessageType

logger = logging.getLogger(__name__)

class Bot(object):

    connection = None

    def __init__(self, name, game_strategy):
        self.name = name
        self.session_name = name
        self.game_strategy = game_strategy
        self.handCards= []

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
            answer = messages.create(MessageType.CHOOSE_SESSION["name"], "AUTOJOIN", self.session_name, "TOURNAMENT", False)
            logger.info('session choice answer: %s', answer)
            
        elif message_type == MessageType.DEAL_CARDS["name"]:
            #CHALLENGE2017: Getting cards from server... just put them to your handcards
            self.handCards = data

        elif message_type == MessageType.REQUEST_TRUMPF["name"]:
            #CHALLENGE2017: Ask the brain which gameMode to choose
            gameMode = self.game_strategy.chooseTrumpf(self.handCards)
            answer = messages.create(MessageType.CHOOSE_TRUMPF["name"], gameMode)
            
        elif message_type == MessageType.REQUEST_CARD["name"]:
            #CHALLENGE2017: Ask the brain which card to choose
            card = self.game_strategy.chooseCard(self.handCards, data)
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
            #CHALLENGE2017: When server sends this, you send an invalid card... this should never happen!
            # Server will send "REQUEST_CARD" after this once. Make sure you choose a valid card or your bot will loose the game
            logger.warning(" ######   SERVER REJECTED CARD   #######")
            pickedCard = self.game_strategy.chooseCard(self.handCards, [])
            logger.warning("Rejected card: %s", data)
            logger.warning("Picked card: %s", pickedCard)
            logger.warning("Hand Cards: %s", self.handCards)
            logger.warning("cardsAtTable %s", self.game_strategy.cardsAtTable)
            logger.warning("Gametype: %s | %s", self.game_strategy.gameType["mode"], self.game_strategy.gameType["trumpfColor"])
            
        elif message_type == MessageType.BROADCAST_GAME_FINISHED["name"]:
            #Do nothing with that :-)
            pass
        elif message_type == MessageType.BROADCAST_SESSION_JOINED["name"]:
            #Do nothing with that :-)
            pass
        elif message_type == MessageType.BROADCAST_STICH["name"]:
            #Do nothing with that :-)
            pass
        elif message_type == MessageType.BROADCAST_TOURNAMENT_STARTED["name"]:
            #Do nothing with that :-)
            pass
        elif message_type == MessageType.BROADCAST_TOURNAMENT_RANKING_TABLE["name"]:
            #Do nothing with that :-)
            pass
        elif message_type == MessageType.BROADCAST_TEAMS["name"]:
            #Do nothing with that :-)
            pass
        elif message_type == MessageType.BROADCAST_TRUMPF["name"]:
            self.game_strategy.gameMode(data)
            pass
        elif message_type == MessageType.BROADCAST_WINNER_TEAM["name"]:
            #Do nothing with that :-)
            pass
        else:
            logger.warning("Sorry, i cannot handle this message: " + json.dumps(message))

        if answer:
            self.connection.send(answer)
