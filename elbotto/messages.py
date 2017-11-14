from enum import Enum

from elbotto.card import Card, Color


class GameType(object):

    def __init__(self, mode, trumpfColor=None):
        self.mode = mode

        if trumpfColor is not None:
            self.trumpf_color = Color[trumpfColor]

    def __repr__(self):
        return "% s | % s"%(self.mode, self.trumpf_color)

    def to_dict(self):
        if hasattr(self, 'trumpf_color'):
            return dict(mode = self.mode,
                    trumpfColor = self.trumpf_color.name)

        return dict(mode=self.mode)

class RoundScore(object):

    def __init__(self, name, points, currentRoundPoints):
        self.team_name = name
        self.total_points = points
        self.current_game_points = currentRoundPoints


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
        return "%s [%s]"%(self.name, self.seatId)


class MessageType(Enum):

    REQUEST_PLAYER_NAME = 'REQUEST_PLAYER_NAME'
    CHOOSE_PLAYER_NAME = 'CHOOSE_PLAYER_NAME'
    BROADCAST_TEAMS = 'BROADCAST_TEAMS'
    DEAL_CARDS = 'DEAL_CARDS'
    REQUEST_TRUMPF = 'REQUEST_TRUMPF'
    CHOOSE_TRUMPF = 'CHOOSE_TRUMPF'
    REJECT_TRUMPF = 'REJECT_TRUMPF'
    BROADCAST_TRUMPF = 'BROADCAST_TRUMPF'
    BROADCAST_STICH = 'BROADCAST_STICH'
    BROADCAST_WINNER_TEAM = 'BROADCAST_WINNER_TEAM'
    BROADCAST_GAME_FINISHED = 'BROADCAST_GAME_FINISHED'
    PLAYED_CARDS = 'PLAYED_CARDS'
    REQUEST_CARD = 'REQUEST_CARD'
    CHOOSE_CARD = 'CHOOSE_CARD'
    REJECT_CARD = 'REJECT_CARD'
    REQUEST_SESSION_CHOICE = 'REQUEST_SESSION_CHOICE'
    CHOOSE_SESSION = 'CHOOSE_SESSION',
    SESSION_JOINED = 'SESSION_JOINED'
    BROADCAST_SESSION_JOINED = 'BROADCAST_SESSION_JOINED'
    BAD_MESSAGE = 'BAD_MESSAGE'
    BROADCAST_TOURNAMENT_RANKING_TABLE = 'BROADCAST_TOURNAMENT_RANKING_TABLE'
    START_TOURNAMENT = 'START_TOURNAMENT',
    BROADCAST_TOURNAMENT_STARTED = 'BROADCAST_TOURNAMENT_STARTED'
    JOIN_BOT = 'JOIN_BOT',


def createRequestPlayerName():
    return dict(
        type = MessageType.REQUEST_PLAYER_NAME
    )

def createChoosePlayerName(playerName):
    return dict(
        type = MessageType.CHOOSE_PLAYER_NAME.name,
        data = playerName
    )

def createBroadcastTeams(data):
    teams = []
    for team_info in data:
        team = Team(team_info["name"], [Player(**player_info) for player_info in team_info["players"]])
        teams.append(team)

    return dict(
        type = MessageType.BROADCAST_TEAMS,
        data = teams
    )

def createDealCards(cards):
    return dict(
        type = MessageType.DEAL_CARDS,
        data = [Card.create(item["number"], item["color"]) for item in cards]
    )

def createRequestTrumpf(geschoben):
    return dict(
        type = MessageType.REQUEST_TRUMPF,
        data = geschoben
    )

def createRejectTrumpf(gameType):
    return dict(
        type = MessageType.REJECT_TRUMPF,
        data = GameType(**gameType)
    )

def createChooseTrumpf(gameType):
    return dict(
        type = MessageType.CHOOSE_TRUMPF.name,
        data = gameType.to_dict()
    )

def createBroadcastTrumpf(gameType):
    return dict(
        type = MessageType.BROADCAST_TRUMPF,
        data = GameType(**gameType)
    )

def createBroadcastStich(data):
    score = [RoundScore(**score) for score in data.pop("teams")]

    return dict(
        type = MessageType.BROADCAST_STICH,
        data = dict(
            score = score,
            playedCards = [Card.create(**card) for card in data.pop("playedCards")],
            winner = Player(**data)
        )
    )

def createBroadcastGameFinished(data):
    return dict(
        type = MessageType.BROADCAST_GAME_FINISHED,
        data = [RoundScore(**score) for score in data]
    )


def createBroadcastWinnerTeam(score):
    return dict(
        type = MessageType.BROADCAST_WINNER_TEAM,
        data = RoundScore(**score)
    )

def createPlayedCards(playedCards):
    return dict(
        type = MessageType.PLAYED_CARDS,
        data = [Card.create(item["number"], item["color"]) for item in playedCards]
    )

def createRequestCard(cards):
    return dict(
        type = MessageType.REQUEST_CARD,
        data = cards
    )

def createChooseCard(card):
    return dict(
        type = MessageType.CHOOSE_CARD.name,
        data = card.to_dict()
    )

def createRejectCard(card):
    return dict(
        type = MessageType.REJECT_CARD,
        data = Card.create(card["number"], card["color"])
    )

def createRequestSessionChoice(*availableSessions):
    return dict(
        type = MessageType.REQUEST_SESSION_CHOICE,
        data = availableSessions
    )

def createChooseSession(sessionChoice="AUTOJOIN", sessionName="Session 1", sessionType="TOURNAMENT", asSpectator=False, chosenTeamIndex=0):
    return dict(
        type = MessageType.CHOOSE_SESSION.name,
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
        type = MessageType.SESSION_JOINED,
        data = {
        sessionName,
        player,
        playersInSession
        }
    )

def createBroadcastSessionJoined(data):
    return dict(
        type = MessageType.BROADCAST_SESSION_JOINED,
        data = {
            "sessionName":data["sessionName"],
            "player": Player(**data["player"]),
            "playersInSession": [Player(**player) for player in data["playersInSession"]]
        }
    )

def createBadMessage(message):
    return dict(
        type = MessageType.BAD_MESSAGE,
        data = message
    )

def createTournamentRankingTable(rankingTable):
    return dict(
        type = MessageType.BROADCAST_TOURNAMENT_RANKING_TABLE,
        data = rankingTable
    )

def createStartTournament():
    return dict(
        type = MessageType.START_TOURNAMENT
    )

def createBroadcastTournamentStarted():
    return dict(
        type = MessageType.BROADCAST_TOURNAMENT_STARTED
    )

def createJoinBot(data):
    return dict(
        type = MessageType.JOIN_BOT,
        data=data
    )
        
def create(type, *args):

    if isinstance(type, MessageType):
        messageType = type
    else:
        try:
            messageType = MessageType[type]
        except:
            raise 'Unknown message type ' + type

    if messageType == MessageType.REQUEST_PLAYER_NAME:
        return createRequestPlayerName()
    elif messageType == MessageType.CHOOSE_PLAYER_NAME:
        return createChoosePlayerName(*args)
    elif messageType == MessageType.BROADCAST_TEAMS:
        return createBroadcastTeams(*args)
    elif messageType == MessageType.DEAL_CARDS:
        return createDealCards(*args)
    elif messageType == MessageType.REQUEST_TRUMPF:
        return createRequestTrumpf(*args)
    elif messageType == MessageType.REJECT_TRUMPF:
        return createRejectTrumpf(*args)
    elif messageType == MessageType.CHOOSE_TRUMPF:
        return createChooseTrumpf(*args)
    elif messageType == MessageType.BROADCAST_TRUMPF:
        return createBroadcastTrumpf(*args)
    elif messageType == MessageType.BROADCAST_WINNER_TEAM:
        return createBroadcastWinnerTeam(*args)
    elif messageType == MessageType.BROADCAST_STICH:
        return createBroadcastStich(*args)
    elif messageType == MessageType.BROADCAST_GAME_FINISHED:
        return createBroadcastGameFinished(*args)
    elif messageType == MessageType.PLAYED_CARDS:
        return createPlayedCards(*args)
    elif messageType == MessageType.REQUEST_CARD:
        return createRequestCard(*args)
    elif messageType == MessageType.CHOOSE_CARD:
        return createChooseCard(*args)
    elif messageType == MessageType.REJECT_CARD:
        return createRejectCard(*args)
    elif messageType == MessageType.REQUEST_SESSION_CHOICE:
        return createRequestSessionChoice(*args)
    elif messageType == MessageType.CHOOSE_SESSION:
        return createChooseSession(*args)
    elif messageType == MessageType.SESSION_JOINED:
        return createSessionJoined(*args)
    elif messageType == MessageType.BROADCAST_SESSION_JOINED:
        return createBroadcastSessionJoined(*args)
    elif messageType == MessageType.BAD_MESSAGE:
        return createBadMessage(*args)
    elif messageType == MessageType.BROADCAST_TOURNAMENT_RANKING_TABLE:
        return createTournamentRankingTable(*args)
    elif messageType == MessageType.START_TOURNAMENT:
        return createStartTournament()
    elif messageType == MessageType.BROADCAST_TOURNAMENT_STARTED:
        return createBroadcastTournamentStarted()
    elif messageType == MessageType.JOIN_BOT:
        return createJoinBot(args)
    else:
        raise 'Unknown message type ' + messageType
