#  Copyright (c) 2020. Rinze Douma

from random import shuffle, randrange


class Card:
    """Class to hold characteristics of playing card."""

    suits = ["spades", "clubs", "hearts", "diamonds"]
    values = [None, "Ace", 2, 3, 4, 5, 6, 7, 8, 9, 10,
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
    def __init__(self, n=6):
        """n Deck of card(s) consisting out of 52 playing cards."""

        c = [Card(v, s) for v in range(2, 15) for s in range(4)]
        self.cards = c * n
        self.reshuffle()
        shoe_size = len(self.cards)
        b_start = int(shoe_size - (shoe_size / n))
        b_end = int(shoe_size - (shoe_size / (n * 2)))
        self.blank = randrange(b_start, b_end)

    def reshuffle(self):
        shuffle(self.cards)

    def deal(self):
        return self.cards.pop()


class Player:
    def __init__(self, name):
        """Class to store name, cards drawn and score of Player."""

        self.hand = []
        self.score = 0
        self.name = name


class Game:
    """Initialize and execute blackjack game."""

    def __init__(self, num_players=2, mode="casino"):
        """Initialize values for game."""

        name_q = "What's the name of player number {}?"
        self.players = []
        for p in range(num_players):
            name = validate_input(name_q.format(str(p+1)))
            self.players[p] = Player(name)
        self.shoe = Deck()
        self.num_players = num_players

    def deal_card(self, player):
        # deal card
        new_card = self.shoe.deal()
        # check score
        if len(player.hand) < 3:
            return
        if new_card.value == 14:
            new_card.value = self.ask_ace(new_card)
        player.hand.append(new_card)
        # check score again
        self.check_score(player.hand)

    def ask_ace(self, c):
        """Ask whether ace counts as 1 or 11."""

        p = (f"You drew an Ace of {Card.suits[c.suit]}. "
             f"Does it count as 1) or 11?")
        choice = validate_input(p, int, options=[1, 11])
        return 1 if choice == 1 else 14

    def check_score(self, player):
        """Returns sum of cards in current hand."""

        for card in player.hand:
            if card == 14:
                player.score += 11
            elif card in [10, 11, 12, 13]:
                player.score += 10
            else:
                player.score += card

    def check_natural(self, player):
        a, b = player.hand
        if ((a.value in [10, 11, 12, 13] and b.value == 14)
                or (b.value in [10, 11, 12, 13] and a.value == 14)):
            return True

    def update_bet(self):
        """Calculate win/lose and update stack"""
        pass

    def play(self):
        """Run the game."""
        # deal first hand
        for p in self.players:
            for i in range(2):
                self.deal_card(p)
            if self.check_natural(p):
                # what to do for natural
                pass
            # Check if ace in first hand
            for card in p.hand:
                if card.value == 14:
                    self.ask_ace(card)
        # dealer first cards
        # check natural
        # for each player deal
        # reshuffle
        pass


def validate_input(prompt, type_=None, min_=None, max_=None, options=None):
    """ Request user input and clean it before return.
    :param prompt: Question to ask user.
    :param type_: Type of value asked. str, int, float.
    :param min_: Minimum length of str of lower value of int.
    :param max_: Maximum length of str of upper value of int.
    :param options: List of options allowed
    :return: str, int or float.
    """
    if (min_ is not None
            and max_ is not None
            and max_ < min_):
        raise ValueError("min_ must be less than or equal to max_.")
    while True:
        ui = input(prompt)
        if type_ is not None:
            try:
                ui = type_(ui)
            except ValueError:
                print(f"Input type must be {type_.__name__}")
                continue
        if isinstance(ui, str):
            ui_num = len(ui)
        else:
            ui_num = ui
        if max_ is not None and ui_num > max_:
            print(f"Input must be less than or equal to {max_}.")
        elif min_ is not None and ui_num < min_:
            print(f"Input must be more than or equal to {min_}.")
        elif options is not None and ui_num not in options:
            print(f"Input must be one of the following:" + " ".join(options))
        else:
            return ui


if __name__ == '__main__':
    """Load game if script executed directly."""

    game = Game()
