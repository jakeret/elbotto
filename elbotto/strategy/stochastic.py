import logging
import random

logger = logging.getLogger(__name__)

class PlayStrategy(object):

    def __init__(self):
        self.geschoben= False
        self.cardsAtTable = []
    
    def chooseTrumpf(self, handcards):
        #CHALLENGE2017: Implement logic to chose game mode which is best suited to your handcards or schiäbä.
        # Consider that this decision ist quite crucial for your bot to be competitive
        # Use hearts as TRUMPF for now
        gameType = {
            "mode": "TRUMPF",
            "trumpfColor": "HEARTS"
        }
        return gameType


    def gameMode(self, gameType):
        self.geschoben = gameType["mode"] == "SCHIEBE" #just remember if it's a geschoben match
        self.gameType = gameType
    
    def chooseCard(self, handcards, tableCards):
        #CHALLENGE2017: Implement logic to choose card so your bot will beat all the others.
        # Keep in mind that your counterpart is another instance of your bot
        validCards = self.getPossibleCards(handcards, tableCards)

        idx = random.randint(0, len(validCards)-1)

        card = validCards[idx]
        logger.info("Chosen card: %s", card)
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