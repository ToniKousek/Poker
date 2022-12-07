# A game of poker
from random import shuffle, seed

# Suites: clubs (♣) == 0, diamonds (♦) == 1, hearts (♥) == 2 and spades (♠) == 3

# constants
starting_money = 5000
smallest_bet = 50
seed(0)  # Remove this in active version


class Card:
    def __init__(self, suite: int, rank: int) -> None:
        self.suite = suite
        self.rank = rank


class Player:
    def __init__(self, id) -> None:
        self.id = id
        self.cards: list[Card] = []
        self.money = starting_money

    def show_cards(self) -> None:
        for card in self.cards:
            if card.rank == 11:  # Jack
                print("Jack of ", end="")
            elif card.rank == 12:  # Queen
                print("Queen of ", end="")
            elif card.rank == 13:  # King
                print("King of ", end="")
            elif card.rank == 14:  # Ace
                print("Ace of ", end="")
            else:
                print(f"{card.rank} of ", end="")

            if card.suite == 0:
                print("clubs(♣)", end="")
            elif card.suite == 1:
                print("diamonds(♦)", end="")
            elif card.suite == 2:
                print("hearts(♥)", end="")
            elif card.suite == 3:
                print("spades(♠)", end="")

            print("\t\t", end="")
        else:
            print()

    def human_choose_action(self):
        print("What would you like to do?")
        print("1 - Bet")


class Deck:
    def __init__(self) -> None:
        self.cards: list[Card] = []

    def init_cards(self) -> None:
        # creating the cards
        self.cards = []
        for i in range(4):  # suites
            for j in range(2, 15):  # ranks
                self.cards.append(Card(i, j))
        shuffle(self.cards)

    def give_cards(self, player: Player) -> None:
        for _ in range(2):
            player.cards.append(self.cards[0])
            self.cards = self.cards[1:]


class Table:
    def __init__(self) -> None:
        self.players: list[Player] = []
        self.round_players: list[Player] = []
        self.cards: list[Card] = []
        self.human_position = 0
        self.num_of_players = 0  # placeholder until init_players()

    def init_players(self, num_of_players) -> None:
        for i in range(num_of_players):
            self.players.append(Player(i))
            self.round_players.append(Player(i))
        self.num_of_players = num_of_players

    def pre_flop(self):
        bet_player = -1
        while True:
            for player in self.round_players[bet_player+1:]+self.round_players[:bet_player+1]:
                if player.id == self.human_position:
                    action = player.human_choose_action()
                    if action == "bet":
                        bet_player = player.id
                        break
                else:
                    # the logic
                    pass

    def flop(self):
        pass

    def turn(self):
        pass

    def river(self):
        pass


def main() -> None:

    # creating the cards
    card_deck = Deck()
    card_deck.init_cards()

    # getting the number of players
    while True:
        print("Enter the number of players including yourself!\nIt must be between 2 and 10 including those!")
        try:
            num_of_players = int(input("Please enter a number: "))
            if (num_of_players >= 2 and num_of_players <= 10):
                break
            print("\n")
        except KeyboardInterrupt:
            print("Exiting!")
            exit()
        except:
            print("Without any letters")
            print("\n")

    print("Setting up the table.")
    # initializing the table
    table = Table()
    table.init_players(num_of_players)

    # Table loop
    while len(table.players) > 1:
        print("Giving the cards to everybody.\n")
        for player in table.players:
            card_deck.give_cards(player)

        print(f"You're going {table.human_position + 1}.")
        print("Your cards are:")
        table.players[table.human_position].show_cards()

        # Round loop
        for betting_round in ["Pre-flop", "Flop", "Turn", "River"]:
            if betting_round == "Pre-flop":
                table.pre_flop()
            elif betting_round == "Flop":
                pass
            elif betting_round == "Turn":
                pass
            elif betting_round == "River":
                pass

        print(table.__dict__)  # Debugging
        # Until the redo rounds mechanic is done
        break


if __name__ == "__main__":
    main()
