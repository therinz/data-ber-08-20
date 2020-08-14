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
    def __init__(self, name, cash, bet):
        """Class to store name, cards drawn and score of Player."""

        self.hand = []
        self.score = 0
        self.name = name
        self.bet = bet
        self.cash = cash


class Game:
    """Initialize and execute blackjack game."""

    def __init__(self, num_players=2, cash=1000, min_bet=100):
        """Initialize values for game."""

        name_q = "What's the name of player number {}?"
        self.players = []
        for p in range(num_players):
            name = validate_input(name_q.format(str(p+1)))
            self.players[p] = Player(name, cash, min_bet)
        self.shoe = Deck()
        self.active = list(self.players)
        self.dealer = Player("Dealer", 1000000, 0)

    def deal_card(self, player, first=False):
        """Deal card, check if ace and check score."""

        # Deal card
        new_card = self.shoe.deal()
        if first:
            # First round: return second card
            return self.shoe.deal()
        # check score
        if new_card.value == 14:
            new_card.value = self.ask_ace(new_card)
        player.hand.append(new_card)
        # check score again
        self.check_score(player.hand)

    def ask_ace(self, c):
        """Ask whether ace counts as 1 or 11."""

        p = (f"You drew an Ace of {Card.suits[c.suit]}. "
             f"Does it count as 1 or 11?")
        choice = validate_input(p, int, options=[1, 11])
        return 1 if choice == 1 else 14

    def check_score(self, player):
        """Updates sum of cards in current hand."""

        for card in player.hand:
            if card == 14:
                player.score += 11
            elif card in [10, 11, 12, 13]:
                player.score += 10
            else:
                player.score += card

    def check_natural(self, player):
        """Check whether player hand qualifies as natural."""

        a, b = player.hand
        if ((a.value in [10, 11, 12, 13] and b.value == 14)
                or (b.value in [10, 11, 12, 13] and a.value == 14)):
            player.score = 21

    def update_bet(self, natural=False):
        """Calculate win/lose and update stack"""

        # First set dealer score to zero if bust
        dealer = self.dealer.score if self.dealer.score < 22 else 0

        # For every player check outcome
        for p in self.players:
            # Only execute if this player or dealer has natural
            if not natural or (natural and dealer != 21):
                continue

            if p.score < dealer or p.score > 21:
                p.cash -= p.bet
                self.dealer.cash += p.bet
            elif p.score > dealer:
                # If player has natural but dealer doesn't then bet * 1,5
                if natural:
                    p.bet *= 1.5
                p.cash += p.bet
                self.dealer.cash -= p.bet

    def first_round(self):
        """Deal first hand to all players and dealer."""

        for p in self.players:
            self.deal_card(p, first=True)
            self.check_natural(p)

            # Check if ace in first hand
            for card in p.hand:
                if card.value == 14:
                    self.ask_ace(card)

        # dealer first cards
        dealer = self.dealer
        self.deal_card(dealer, first=True)
        self.check_natural(dealer)
        if any([p.score for p in self.players] + [self.dealer.score]):
            self.update_bet(natural=True)

    def play_round(self):
        """After first cards each players goes a round"""

        prompt = "Stand (s) or hit (h)?"
        s_or_h = ["stand", "hit", "s", "h"]

        for p in self.active:
            while p.score < 21:
                q = validate_input(prompt, str, options=s_or_h)
                if q in ["hit", "h"]:
                    self.deal_card(p)
                else:
                    self.active.remove(p)
                    break

        # Dealer must stand when 17 or over
        d = self.dealer
        while d.score < 17:
            self.deal_card(d)
            # Ace counts as 11 when total would be between 16 & 22
            if 1 in d.hand:
                if 16 < sum(d.hand + [10]) < 22:
                    break

    def reset_players(self):
        for p in self.players:
            p.hand.clear()
            p.score = 0
        self.active = list(self.players)

    def play(self):
        """Run the game and clean up after"""

        self.first_round()
        self.play_round()
        self.update_bet()
        self.reset_players()

        # If blank card has been reached then reshuffle
        if self.shoe.blank:
            self.shoe.reshuffle()


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
        elif options is not None and ui not in options:
            print(f"Input must be one of the following:" + " ".join(options))
        else:
            return ui


if __name__ == '__main__':
    """Load game if script executed directly."""

    game = Game()
