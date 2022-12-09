# A game of poker
from random import shuffle, seed

# Suites: clubs (♣) == 0, diamonds (♦) == 1, hearts (♥) == 2 and spades (♠) == 3

# constants
starting_money = 5000
smallest_bet = 50
seed(0)  # Remove this in active version

# bug with no cards printed on the action


class Card:
    def __init__(self, suite: int, rank: int) -> None:
        self.suite = suite
        self.rank = rank


class Player:
    def __init__(self, id) -> None:
        self.id: int = id  # id of 0 is human player
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

    def human_choose_action(self, min_bet: int, table):
        print("What would you like to do?\n")
        print("Check your cards - 1")
        print("Check the cards on the table - 2")
        print("Check your money - 3")
        print("Bet - 4")
        print("Fold - 5")
        if min_bet == 0:
            print("Check - 6")

        # checking that the input is correct
        while True:
            try:
                action = int(input())
                if action < 1 or action > 5 + (min_bet == 0):
                    raise ValueError
                break
            except KeyboardInterrupt:
                exit()
            except:
                print(
                    f"Please input a number between 1 and {2 + (min_bet == 0)} only!")

        # default checks
        if action == 1:
            print("Your cards are:")
            self.show_cards()
            print(self.cards)
            self.human_choose_action(min_bet, table)
        elif action == 2:
            table.show_cards()
            self.human_choose_action(min_bet, table)
        elif action == 3:
            print(f"You have {self.money} tokens!")
            self.human_choose_action(min_bet, table)

        # main checks
        elif action == 4:  # bet
            print("You selected bet!")
            print("How much would you like to bet")
            print("Go back - 0 ")
            while True:
                try:
                    amount = int(input())
                    if amount < smallest_bet or amount > self.money:
                        raise ValueError
                    elif amount == 0:
                        print("Going back!")
                        self.human_choose_action(min_bet, table)
                        return
                    break
                except KeyboardInterrupt:
                    exit()
                except:
                    print(
                        f"Please input a number between {smallest_bet} and {self.money} only!\nOr 0 to go back")

            print(f"You just bet {amount}!")
            print("\nDeducting the money\n")  # TODO Delete on production

            # deducting money
            self.money -= amount
            table.pot = amount
            table.curr_bet = amount
        elif action == 5:  # fold
            print("You selected fold!")
            table.fold(self)
        elif action == 6:
            print("You knock on the wooden table to signify a check!")
        return action

    def ai_choose_action(self, min_bet: int):
        return


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
        self.curr_bet = 0
        self.pot = 0
        self.human_position = 0
        self.num_of_players = 0  # placeholder until init_players()

    def init_players(self, num_of_players) -> None:
        for i in range(num_of_players):
            self.players.append(Player(i))
            self.round_players.append(Player(i))
        self.num_of_players = num_of_players

    def show_cards(self) -> None:
        if self.cards == []:
            print("There are no cards!")
            return
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
                print("clubs(♣)")
            elif card.suite == 1:
                print("diamonds(♦)")
            elif card.suite == 2:
                print("hearts(♥)")
            elif card.suite == 3:
                print("spades(♠)")
        else:
            print()

    def fold(self, player: Player):
        player.cards = []

    def pre_flop(self, start_position: int):
        print("It's the preflop round!")
        print(
            f"You're {(self.human_position + start_position) % self.num_of_players + 1}.")  # The position of the human player

        # starting the loop with the player who betted last + 1
        # now we get the id of the player who is supposed to bet or check
        for player_id in [(i.id + start_position + 1) % self.num_of_players for i in self.round_players]:
            # simplification to get the player and not the id
            player = self.round_players[0]  # could be unbound
            for i in self.round_players:
                if i.id == player_id:
                    player = i
            if player.id == 0:  # human
                player.human_choose_action(self.curr_bet, self)
            else:
                player.ai_choose_action(self.curr_bet)

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
    # while len(table.players) > 1:
    while True:
        print("Giving the cards to everybody.\n")
        for player in table.players:
            card_deck.give_cards(player)
            print(player.__dict__)

        print(f"You're going {table.human_position + 1}.")
        print("Your cards are:")
        table.players[table.human_position].show_cards()

        # Round loop
        for betting_round in ["Pre-flop", "Flop", "Turn", "River"]:
            if betting_round == "Pre-flop":
                # -1 because in the func is a +1 and we have to get the 0th
                table.pre_flop(-1)
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
