#  Copyright (c) 2020. Rinze Douma

from random import shuffle


class Card:
    """Class to hold characteristics of playing card."""

    suits = ["spades", "clubs", "hearts", "diamonds"]
    values = [None, None, 2, 3, 4, 5, 6, 7, 8, 9, 10,
              "Jack", "Queen", "King", "Ace"]

    def __init__(self, v, s):
        self.value = v
        self.suit = s

    def __lt__(self, other):
        """Returns True if card is lower than other card."""

        if self.value < other.value:
            return True
        if self.value == other.value:
            return True if self.suit > other.suit else False

    def __gt__(self, other):
        if self.value > other.value:
            return True

    def __str__(self):
        """String representation of playing card."""

        return f"{Card.values[self.value]} of {Card.suits[self.suit]}"


class Deck:
    def __init__(self, n=1):
        """n Deck of card(s) consisting out of 52 playing cards."""

        c = [Card(v, s) for v in range(2, 15) for s in range(4)]
        self.cards = c * n
        shuffle(c * 4)


class Player:
    def __init__(self, name):
        """Class to store name, cards drawn and wins of Player."""

        self.wins = 0
        self.card = []
        self.name = name


class Game:
    """Initialize and execute blackjack game."""

    def __init__(self, players=2, mode="casino"):
        """Initialize values for game."""

        name_q = "What's the name of player number {}?"
        self.player = []
        for p in range(players):
            name = input(name_q.format(str(p+1)))
            self.player[p] = Player(name)
        self.shoe = Deck()


if __name__ == '__main__':
    """Load game if script executed directly."""

    game = Game()
