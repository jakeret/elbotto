
HEARTS= "HEARTS"
DIAMONDS= "DIAMONDS"
CLUBS= "CLUBS"
SPADES= "SPADES"

class Card(object):

    def __init__(self, number, color):
        self.number = number
        self.color = color

    @staticmethod
    def create(number, color):
        return Card(number, color)

    def __eq__(self, other):
        return self.number == other.number and self.color == other.color

    def to_dict(self):
        return dict(number=self.number,
                    color=self.color)

    def __repr__(self):
        return "%s - %s"%(self.number, self.color)