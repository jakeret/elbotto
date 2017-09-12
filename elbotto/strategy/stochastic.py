import logging
import random

from elbotto import messages
from elbotto.basebot import BaseBot, DEFAULT_TRUMPF
from elbotto.messages import MessageType

logger = logging.getLogger(__name__)


class Bot(BaseBot):

    def __init__(self, name):
        super(Bot, self).__init__(name)
        self.game_strategy = PlayStrategy()

    def handle_request_trumpf(self, answer):
        # CHALLENGE2017: Ask the brain which gameMode to choose
        gameMode = self.game_strategy.chooseTrumpf(self.handCards)
        answer = messages.create(MessageType.CHOOSE_TRUMPF["name"], gameMode)
        return answer

    def handle_stich(self, won, winner, round_points, total_points):
        logger.info("Stich: Won:%s, Winner: %s, Round points: %s, Total points: %s", won, winner, round_points, total_points)

    def handle_game_finished(self):
        # Do nothing with that :-)
        pass

    def handle_reject_card(self, data):
        # CHALLENGE2017: When server sends this, you send an invalid card... this should never happen!
        # Server will send "REQUEST_CARD" after this once. Make sure you choose a valid card or your bot will loose the game
        logger.warning(" ######   SERVER REJECTED CARD   #######")
        pickedCard = self.game_strategy.chooseCard(self.handCards, [])
        logger.debug("Rejected card: %s", data)
        logger.debug("Picked card: %s", pickedCard)
        logger.debug("Hand Cards: %s", self.handCards)
        logger.debug("cardsAtTable %s", self.game_strategy.cardsAtTable)
        logger.debug("Gametype: %s", self.game_type)

    def handle_request_card(self, data):
        # CHALLENGE2017: Ask the brain which card to choose
        card = self.game_strategy.chooseCard(self.handCards, data)
        answer = messages.create(MessageType.CHOOSE_CARD["name"], card)
        return answer


class PlayStrategy(object):

    def __init__(self):
        self.geschoben= False
        self.cardsAtTable = []

    def chooseTrumpf(self, handcards):
        #CHALLENGE2017: Implement logic to chose game mode which is best suited to your handcards or schiäbä.
        # Consider that this decision ist quite crucial for your bot to be competitive
        # Use hearts as TRUMPF for now
        return DEFAULT_TRUMPF

    def chooseCard(self, handcards, tableCards):
        #CHALLENGE2017: Implement logic to choose card so your bot will beat all the others.
        # Keep in mind that your counterpart is another instance of your bot
        validCards = self.getPossibleCards(handcards, tableCards)

        idx = random.randint(0, len(validCards)-1)

        card = validCards[idx]
        logger.debug("Chosen card: %s", card)
        return card

    def getPossibleCards(self, handCards, tableCards):
        # validation = Validation.create(self.gameType.mode, self.gameType.trumpfColor)
        # possibleCards = handCards.filter(function (card) {
        #     if (validation.validate(tableCards, handCards, card)) {
        #         return true
        #     }
        # }, this)

        # return possibleCards
        return handCards

    # def setValidation(self, gameMode, trumpfColor):
    #     self.validation = Validation.create(gameMode, trumpfColor)