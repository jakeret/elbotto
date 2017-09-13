from elbotto.card import Card, Color


class GameType(object):

    def __init__(self, mode, trumpfColor):
        self.mode = mode
        self.trumpf_color = Color[trumpfColor]

    def __repr__(self):
        return "% s | % s"%(self.mode, self.trumpf_color)

    def to_dict(self):
        return dict(mode = self.mode,
                    trumpfColor = self.trumpf_color.name)

class RoundScore(object):

    def __init__(self, name, points, currentRoundPoints):
        self.team_name = name
        self.points = points
        self.current_round_points = currentRoundPoints


class Team(object):

    def __init__(self, name, players):
        self.name = name
        self.players = players

    def is_member(self, player):
        for member in self.players:
            if member.id == player.id:
                return True

        return False

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return "%s %s"%(self.name, self.players)


class Player(object):

    def __init__(self, id, seatId, name):
        self.id = id
        self.seatId = seatId
        self.name = name

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        return "%s [%s] [%s]"%(self.name, self.seatId, self.id)


class MessageType(object):
    
    REQUEST_PLAYER_NAME = dict( 
        name = 'REQUEST_PLAYER_NAME'
    )

    CHOOSE_PLAYER_NAME = dict( 
        name = 'CHOOSE_PLAYER_NAME',
        constraints = dict( 
            type = dict( 
                presence = True
            ),
            data = dict( 
                presence = True,
                length = dict( 
                    minimum = 1
                )
            )
        )
    )
    BROADCAST_TEAMS = dict( 
        name = 'BROADCAST_TEAMS'
    )

    DEAL_CARDS = dict( 
        name = 'DEAL_CARDS'
    )

    REQUEST_TRUMPF = dict( 
        name = 'REQUEST_TRUMPF'
    )

    CHOOSE_TRUMPF = dict( 
        name = 'CHOOSE_TRUMPF',
        constraints = dict( 
            type = dict( 
                presence = True
            ),
            # data_mode = dict(
            #     presence = True,
            #     inclusion = dict(
            #         within = GameMode
            #     )
            # ),
            # data_trumpfColor = dict(
            #     inclusion = dict(
            #         within = CardColor
            #     )
            # )
        )
    )
    REJECT_TRUMPF = dict( 
        name = 'REJECT_TRUMPF'
    )

    BROADCAST_TRUMPF = dict( 
        name = 'BROADCAST_TRUMPF'
    )

    BROADCAST_STICH = dict( 
        name = 'BROADCAST_STICH'
    )

    BROADCAST_WINNER_TEAM = dict( 
        name = 'BROADCAST_WINNER_TEAM'
    )

    BROADCAST_GAME_FINISHED = dict( 
        name = 'BROADCAST_GAME_FINISHED'
    )

    PLAYED_CARDS = dict( 
        name = 'PLAYED_CARDS'
    )

    REQUEST_CARD = dict( 
        name = 'REQUEST_CARD'
    )

    CHOOSE_CARD = dict(
        name = 'CHOOSE_CARD',
        constraints = dict(
            type = dict(
                presence = True
            ),
            data_number = dict(
                presence = True,
                inclusion = dict(
                    within = [6,7,8,9,10,11,12,13,14]
                )
            ),
            data_color = dict(
                presence = True,
                # inclusion = dict(
                #     within = CardColor
                # )
            )
        )
    )

    REJECT_CARD = dict( 
        name = 'REJECT_CARD'
    )

    REQUEST_SESSION_CHOICE = dict( 
        name = 'REQUEST_SESSION_CHOICE'
    )

    CHOOSE_SESSION = dict(
        name = 'CHOOSE_SESSION',
        constraints = dict(
            type = dict(
                presence = True
            ),
            # data_sessionChoice = dict(
            #     presence = True,
            #     inclusion = dict(
            #         within = SessionChoice
            #     )
            # ),
            # data_sessionName = dict(
            #     length = dict(
            #         minimum = 1
            #     )
            # ),
            # data_sessionType = dict(
            #     inclusion = dict(
            #         within = SessionType
            #     )
            # ),
            # data_chosenTeamIndex = dict(
            #     inclusion = dict(
            #         within = [0, 1]
            #     )
            # ),
            # data_asSpectator = dict(
            #     presence = False
            # )
        )
    )
    SESSION_JOINED = dict( 
        name = 'SESSION_JOINED'
    )

    BROADCAST_SESSION_JOINED = dict( 
        name = 'BROADCAST_SESSION_JOINED'
    )

    BAD_MESSAGE = dict( 
        name = 'BAD_MESSAGE'
    )

    BROADCAST_TOURNAMENT_RANKING_TABLE = dict( 
        name = 'BROADCAST_TOURNAMENT_RANKING_TABLE'
    )

    START_TOURNAMENT = dict(
        name = 'START_TOURNAMENT',
        constraints = dict(
            type = dict(
                presence = True
            )
        )
    )

    BROADCAST_TOURNAMENT_STARTED = dict( 
        name = 'BROADCAST_TOURNAMENT_STARTED'
    )

    JOIN_BOT = dict(
        name = 'JOIN_BOT',
        constraints = dict(
            type = dict(
                presence = True
            ),
            data_sessionName = dict(
                presence = True
            ),
            data_chosenTeamIndex = dict(
                inclusion = dict(
                    within = [0, 1]
                )
            )
        )
    )



def createRequestPlayerName():
    return dict(
        type = MessageType.REQUEST_PLAYER_NAME["name"]
    )

def createChoosePlayerName(playerName):
    return dict(
        type = MessageType.CHOOSE_PLAYER_NAME["name"],
        data = playerName
    )

def createBroadcastTeams(data):
    teams = []
    for team_info in data:
        team = Team(team_info["name"], [Player(**player_info) for player_info in team_info["players"]])
        teams.append(team)

    return dict(
        type = MessageType.BROADCAST_TEAMS["name"],
        data = teams
    )

def createDealCards(cards):
    return dict(
        type = MessageType.DEAL_CARDS["name"],
        data = [Card.create(item["number"], item["color"]) for item in cards]
    )

def createRequestTrumpf(geschoben):
    return dict(
        type = MessageType.REQUEST_TRUMPF["name"],
        data = geschoben
    )

def createRejectTrumpf(gameType):
    return dict(
        type = MessageType.REJECT_TRUMPF["name"],
        data = GameType(**gameType)
    )

def createChooseTrumpf(gameType):
    return dict(
        type = MessageType.CHOOSE_TRUMPF["name"],
        data = gameType.to_dict()
    )

def createBroadcastTrumpf(gameType):
    return dict(
        type = MessageType.BROADCAST_TRUMPF["name"],
        data = GameType(**gameType)
    )

def createBroadcastStich(data):
    score = [RoundScore(**score) for score in data.pop("teams")]

    return dict(
        type = MessageType.BROADCAST_STICH["name"],
        data = dict(
            score = score,
            playedCards = [Card.create(**card) for card in data.pop("playedCards")],
            winner = Player(**data)
        )
    )

def createBroadcastGameFinished(data):
    return dict(
        type = MessageType.BROADCAST_GAME_FINISHED["name"],
        data = [RoundScore(**score) for score in data]
    )


def createBroadcastWinnerTeam(score):
    return dict(
        type = MessageType.BROADCAST_WINNER_TEAM["name"],
        data = RoundScore(**score)
    )

def createPlayedCards(playedCards):
    return dict(
        type = MessageType.PLAYED_CARDS["name"],
        data = [Card.create(item["number"], item["color"]) for item in playedCards]
    )

def createRequestCard(cards):
    return dict(
        type = MessageType.REQUEST_CARD["name"],
        data = cards
    )

def createChooseCard(card):
    return dict(
        type = MessageType.CHOOSE_CARD["name"],
        data = card.to_dict()
    )

def createRejectCard(card):
    return dict(
        type = MessageType.REJECT_CARD["name"],
        data = Card.create(card["number"], card["color"])
    )

def createRequestSessionChoice(*availableSessions):
    return dict(
        type = MessageType.REQUEST_SESSION_CHOICE["name"],
        data = availableSessions
    )

def createChooseSession(sessionChoice="AUTOJOIN", sessionName="Session 1", sessionType="TOURNAMENT", asSpectator=False, chosenTeamIndex=0):
    return dict(
        type = MessageType.CHOOSE_SESSION["name"],
        data = dict(
            sessionChoice=sessionChoice,
            sessionName=sessionName,
            sessionType=sessionType,
            asSpectator=asSpectator,
            chosenTeamIndex=chosenTeamIndex
        )
    )

def createSessionJoined(sessionName, player, playersInSession):
    return dict(
        type = MessageType.SESSION_JOINED["name"],
        data = {
        sessionName,
        player,
        playersInSession
        }
    )

def createBroadcastSessionJoined(data):
    return dict(
        type = MessageType.BROADCAST_SESSION_JOINED["name"],
        data = {
            "sessionName":data["sessionName"],
            "player": Player(**data["player"]),
            "playersInSession": [Player(**player) for player in data["playersInSession"]]
        }
    )

def createBadMessage(message):
    return dict(
        type = MessageType.BAD_MESSAGE["name"],
        data = message
    )

def createTournamentRankingTable(rankingTable):
    return dict(
        type = MessageType.BROADCAST_TOURNAMENT_RANKING_TABLE["name"],
        data = rankingTable
    )

def createStartTournament():
    return dict(
        type = MessageType.START_TOURNAMENT["name"]
    )

def createBroadcastTournamentStarted():
    return dict(
        type = MessageType.BROADCAST_TOURNAMENT_STARTED["name"]
    )

def createJoinBot(data):
    return dict(
        type = MessageType.JOIN_BOT["name"],
        data=data
    )
        
def create(messageType, *args):
    if messageType == MessageType.REQUEST_PLAYER_NAME["name"]:
        return createRequestPlayerName()
    elif messageType == MessageType.CHOOSE_PLAYER_NAME["name"]:
        return createChoosePlayerName(*args)
    elif messageType == MessageType.BROADCAST_TEAMS["name"]:
        return createBroadcastTeams(*args)
    elif messageType == MessageType.DEAL_CARDS["name"]:
        return createDealCards(*args)
    elif messageType == MessageType.REQUEST_TRUMPF["name"]:
        return createRequestTrumpf(*args)
    elif messageType == MessageType.REJECT_TRUMPF["name"]:
        return createRejectTrumpf(*args)
    elif messageType == MessageType.CHOOSE_TRUMPF["name"]:
        return createChooseTrumpf(*args)
    elif messageType == MessageType.BROADCAST_TRUMPF["name"]:
        return createBroadcastTrumpf(*args)
    elif messageType == MessageType.BROADCAST_WINNER_TEAM["name"]:
        return createBroadcastWinnerTeam(*args)
    elif messageType == MessageType.BROADCAST_STICH["name"]:
        return createBroadcastStich(*args)
    elif messageType == MessageType.BROADCAST_GAME_FINISHED["name"]:
        return createBroadcastGameFinished(*args)
    elif messageType == MessageType.PLAYED_CARDS["name"]:
        return createPlayedCards(*args)
    elif messageType == MessageType.REQUEST_CARD["name"]:
        return createRequestCard(*args)
    elif messageType == MessageType.CHOOSE_CARD["name"]:
        return createChooseCard(*args)
    elif messageType == MessageType.REJECT_CARD["name"]:
        return createRejectCard(*args)
    elif messageType == MessageType.REQUEST_SESSION_CHOICE["name"]:
        return createRequestSessionChoice(*args)
    elif messageType == MessageType.CHOOSE_SESSION["name"]:
        return createChooseSession(*args)
    elif messageType == MessageType.SESSION_JOINED["name"]:
        return createSessionJoined(*args)
    elif messageType == MessageType.BROADCAST_SESSION_JOINED["name"]:
        return createBroadcastSessionJoined(*args)
    elif messageType == MessageType.BAD_MESSAGE["name"]:
        return createBadMessage(*args)
    elif messageType == MessageType.BROADCAST_TOURNAMENT_RANKING_TABLE["name"]:
        return createTournamentRankingTable(*args)
    elif messageType == MessageType.START_TOURNAMENT["name"]:
        return createStartTournament()
    elif messageType == MessageType.BROADCAST_TOURNAMENT_STARTED["name"]:
        return createBroadcastTournamentStarted()
    elif messageType == MessageType.JOIN_BOT["name"]:
        return createJoinBot(args)
    else:
        raise 'Unknown message type ' + messageType
