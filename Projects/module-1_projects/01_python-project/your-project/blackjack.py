#  Copyright (c) 2020. Rinze Douma

from random import shuffle, randrange


# Constants
NUM_PLAYERS = 2
CASH = 1000
BET = 100


class Card:
    """Class to hold characteristics of playing card."""

    suits = ["Spades", "Clubs", "Hearts", "Diamonds"]
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
        """"""

        # Create n decks of cards consisting of 52 playing cards each.
        c = [Card(v, s) for v in range(2, 15) for s in range(4)]
        self.cards = c * n
        shuffle(self.cards)

        # A blank signals when the deck should be renewed.
        shoe_size = len(self.cards)
        b_start = int(shoe_size / (n * 2))
        b_end = int(shoe_size / n)
        self.blank = randrange(b_start, b_end)
        self.renew = False

    def deal(self):
        """Check if blank card reached and return a card."""

        if len(self.cards) < self.blank:
            self.renew = True
        return self.cards.pop()


class Player:
    def __init__(self, name, cash, bet):
        """Class to store name, cards drawn and score of Player."""

        self.hand = []
        self.score = 0
        self.name = name
        self.bet = bet
        self.cash = cash
        # Win status. 0: tie, 1: win, 2: loss, 3: natural
        self.win = 0

    def full_hand(self):
        """Return list of card values in current hand."""

        return [c.value for c in self.hand]


class Game:
    """Initialize and execute blackjack game."""

    def __init__(self, num_players=2, cash=1000, min_bet=100):
        """Initialize values for game."""

        self.min_bet = min_bet
        self.cash = cash
        self.num_players = num_players
        self.players = []
        self.welcome()
        self.shoe = Deck()
        self.dealer = Player("Dealer", 1000000, 0)
        self.active = list(self.players)

    def welcome(self):
        """Display game rules and ask for player names."""

        print("\nWelcome to Ironhack Blackjack.")
        print(f"\nHouse rules:"
              f"\n- {self.num_players} Players"
              f"\n- ${self.cash} per player"
              f"\n- ${self.min_bet} bet"
              f"\n- Natural (blackjack on first hand) wins 1,5x of player bet"
              f"\n\n- Enjoy the game and best of luck!\n")
        name_q = "What's the name of player number {}? "
        for p in range(self.num_players):
            name = validate_input(name_q.format(str(p + 1)))
            self.players.append(Player(name, self.cash, self.min_bet))
        print("\n")

    def check_ace(self, p, c):
        """If already an ace in player hand, second will count as 1."""

        if c.value == 14:
            c.value = 1 if 14 in p.full_hand() else 14
        return c

    def deal_card(self, p, num=1):
        """Deal card. Twice if first round otherwise check score."""

        # Deal card
        for i in range(num):
            p.hand.append(self.check_ace(p, self.shoe.deal()))

        # Check score
        self.check_score(p)

        # In first round check hand after second card
        if num > 1:
            self.check_natural(p)
            print(self.hand_details(p, first=True))

    def check_score(self, p):
        """Updates sum of cards in current hand."""

        # Recalculate player score
        p.score = 0
        for card in p.hand:
            # If full ace takes player over 21, count it as a 1
            if card.value == 14 and p.score <= 10:
                p.score += 11
            elif card.value in [10, 11, 12, 13]:
                p.score += 10
            else:
                p.score += card.value

        # If earlier ace would cause >21, change it to a 1
        if p.score > 21 and 14 in p.full_hand():
            for c in p.hand:
                if c.value == 14:
                    c.value = 1
            p.score -= 10
        elif p.score > 21:
            p.score = 0

    def check_natural(self, p):
        """Print if player/dealer has a natural."""

        if p.score == 21:
            print(f"{p.name} drew a Natural!")

    def update_bet(self, natural=False):
        """Calculate win/lose and update cash of every player."""

        for p in self.players:
            # In Natural mode only execute if this player or dealer has 21
            if natural and (self.dealer.score != 21 and p.score != 21):
                continue

            # TODO cash after game
            # Player loses
            if 0 < p.score < self.dealer.score:
                # Dealer wins
                p.cash -= p.bet
                self.dealer.cash += p.bet
                p.win = 2

            # Player win
            elif p.score > self.dealer.score:
                p.win = 1
                bet = p.bet
                if natural:
                    # If player has natural but dealer doesn't then bet * 1,5
                    bet *= 1.5
                    p.win = 3
                    self.active.remove(p)
                p.cash += bet
                self.dealer.cash -= bet

    def hand_details(self, p, first=False):
        """Print details of current hand."""
        # TODO different text for 2nd card
        #  - remove either text for ace

        # In first round show only 1 round if not a Natural
        if p.name == "Dealer":
            if first and p.score != 21:
                dealer_hand = str(p.hand[0])
                d_score = p.hand[0].value
            else:
                dealer_hand = ", ".join([str(c) for c in p.hand])
                d_score = p.score
            text = f"Dealer hand is currently {d_score}: {dealer_hand}"
            return text

        # For players
        begin = f"{p.name}, your current hand is "
        if 14 in [c.value for c in p.hand] and p.score != 21:
            text = f"either {p.score - 10} or {p.score}: "
        else:
            text = f"{p.score}: "
        cards = ", ".join([str(c) for c in p.hand])

        return begin + text + cards

    def first_round(self):
        """Deal first hand to all players and dealer."""

        for p in self.players:
            self.deal_card(p, num=2)

        # Dealer first cards
        self.deal_card(self.dealer, num=2)

        # Update bets if any Natural drawn
        p_nat = [True if p.score == 21 else False for p in self.players]
        if any(p_nat + [self.dealer.score == 21]):
            self.update_bet(natural=True)

            # End round if dealer Natural. Player natural is done in update_bet
            if self.dealer.score == 21:
                self.end_or_continue()

    def play_round(self):
        """After first cards each players goes a round"""

        s_or_h = ["hit", "h", "stand", "s"]

        for p in self.active:
            print("")

            # Ask to deal a card to every active player
            while 0 < p.score < 21:
                prompt = (f"{p.name}, you're now at {p.score}. "
                          f"Do you want to stand (s) or hit (h)?")
                q = validate_input(prompt, str, options=s_or_h)
                if q in s_or_h[:2]:
                    self.deal_card(p)
                    print(self.hand_details(p))
                else:
                    break

            # Feedback to player after choice
            if p.score == 21:
                txt = f"Blackjack! Well done {p.name}."
            elif p.score == 0:
                txt = f"Busted! {p.name}'s bet goes to the house."
            else:
                txt = f"Good choice. Moving on."
            print(txt)
            self.update_bet()

        # Dealer must stand when 17 or over
        d = self.dealer
        print("\nNow to see if its enough.")
        # TODO - other dealer card
        #  - text if dealer stands

        while 0 < d.score < 17:
            self.deal_card(d)
            print(self.hand_details(d))

            # Ace counts as 11 when total would be between 16 & 22
            dealer_hand = d.full_hand()
            if 14 in dealer_hand:
                if 16 < (sum(dealer_hand) + 10) < 22:
                    break

        # Finally update all bets
        self.update_bet()

    def end_or_continue(self):
        """Ask to end game or continue playing."""

        prompt = f"\nWould you like to continue playing?"
        y_n = ["yes", "y", "no", "n", ]
        q = validate_input(prompt, str, options=y_n)

        if q in y_n[:2]:
            self.reset_players()
            self.play()

    def reset_players(self):
        for p in self.players:
            p.hand.clear()
            p.score = 0

        self.active = list(self.players)

    def game_stats(self):
        """Show score and cash of players ."""

        print("\n\nGame stats:")
        print(f"Dealer has a score of {self.dealer.score}.")
        w_l = {0: "kept", 1: "won", 2: "lost", 3: "took 1,5x"}
        for p in self.players:
            print("\n{} has a score of {} and {} their bet of {}."
                  .format(p.name, p.score, w_l[p.win], p.bet))
            print(f"Current cash is {p.cash}")

    def play(self):
        """Run the game and clean up after."""

        self.first_round()
        self.play_round()
        self.game_stats()

        # If blank card has been reached then renew the deck
        if self.shoe.renew:
            self.shoe = Deck()

        self.end_or_continue()


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
        elif options is not None and ui.lower() not in options:
            print("Input must be one of the following:" + ", ".join(options))
        else:
            return ui


if __name__ == '__main__':
    """Load game if script executed directly."""

    game = Game()
    game.play()
