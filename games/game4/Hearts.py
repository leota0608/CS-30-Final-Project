import random as rd
import time as tm

from games.common.GameHandler import GameHandler
from games.game4.HeartsGameData import HeartsGameData
from games.game4.HeartsBot import HeartsBot
from games.game4.HeartsHumanPlayer import HeartsHumanPlayer
from games.common.GameCard import *
from games.teller.Teller import Teller
import games.common.Name as nm

class Hearts(GameHandler):
    def __init__(self, user):

        # the actual user
        self.user = user

        # initializing players
        self.players = [None, None, None, None]
        names = nm.select_name(self.user.name, 3)
        for i in range(3):
            self.players[i] = HeartsBot(names[i])
        self.players[3] = HeartsHumanPlayer(self.user.name)

        # initializing game data
        self.data = HeartsGameData()
        self.initGameData()
        self.rules = Teller("games/game4/rules.txt")

        super().__init__(self.players, self.data)

    def initGameData(self):
        # initializing cards
        for player in self.players:
            self.data.cards.update({player.name: dict()})
            self.data.scores.update({player.name: 0})
            self.data.table.append(None)
            for kind in GameCard.KINDS:
                self.data.cards[player.name].update({kind: list()})

    def distributeCards(self):

        deck = generateDeck()
        rd.shuffle(deck)
        count = len(deck) // len(self.players)

        print("-- let's distribute the cards --")
        print(" --- shuffling, shuffling, shuffling ---")
        tm.sleep(1)

        for player in self.players:
            cards = self.data.cards[player.name]
            for i in range(count):
                chosen = deck.pop()
                suit = chosen.getKindName(chosen.kind)
                cards[suit].append(chosen)

        print(f"each player got {count}.")
        print("be sure to not reveal your cards ...")
        tm.sleep(1)
        print("or else ... ")
        tm.sleep(1)
        print()

    def addCards(self, cards_, name):
        """ adds a given list of cards to a given
        player's card list.
        """
        player_cards = self.data.cards[name]

        for card in cards_:
            suit = GameCard.getKindName(card.kind)
            player_cards[suit].append(card)

    def findStarterPlayer(self):
        """
        finds the index of the player who will start
        the game first. The player with Spade two would start
        the game.
        """

        SPADE_TWO = GameCard("spade", "two")

        for i in range(len(self.players)):
            name = self.players[i].name
            cards = self.data.cards[name]
            for suit in cards:
                for card in cards[suit]:
                    if card == SPADE_TWO:
                        self.data.starter_player = i
        name = self.players[self.data.starter_player].name

        print(f"lucky you player, {name}.")
        print(f"you will start the game first.")
        tm.sleep(1)
        print()

    def exchangeCards(self):
        print(" --- its time to exchange cards ---")

        cards_to_change = []

        for player in self.players:
            print(f"player {player.name} please pick your three cards to exchange.")
            cards_to_change.append(player.provoke("exchange"))
            tm.sleep(1)
            print("thanks!")

        print("exchanging cards ...")
        tm.sleep(2)
        for i in range(len(self.players) - 2, -1, -1):
            prev = i + 1
            self.addCards(cards_to_change[prev], self.players[i].name)
        self.addCards(cards_to_change[0], self.players[len(self.players) - 1].name)
        print("cards had been exchanged")
        print()

    def printPlayerCards(self):
        for player in self.data.cards:
            print(player)
            for kind in self.data.cards[player]:
                for card in self.data.cards[player][kind]:
                    print(card)

    def decideRoundWinner(self):
        """
        decides the winner of the game by finding
        the player who played the highest rank with the
        same kind(suit) as the first player.
        """
        starter = self.data.starter_player
        table = self.data.table
        # this suit is not in terms of string value
        suit = table[starter].kind
        rank = table[starter].rank
        winner = starter

        for i in range(len(self.players)):
            if table[i].kind == suit:
                if table[i].rank > rank:
                    rank = table[i].rank
                    winner = i

        return winner

    def findScore(self, name):
        score = 0
        for card in self.data.table:
            if card.kind == GameCard.KINDS["heart"]:
                score += 1
            elif card == GameCard("spade", "queen"):
                score += 13
        self.data.scores[name] += score

    def askPlayers(self):
        rounds = 52 // len(self.players)

        for round_ in range(rounds):
            print(f"------ round {round_} --------")
            # self.printPlayerCards()
            starter = self.data.starter_player
            for i in range(starter, len(self.players)):
                print(f"player {self.players[i].name}, put your card> ")
                self.data.table[i] = self.players[i].provoke("play")
                print(f"player {self.players[i].name} played {self.data.table[i]}.")

            for i in range(0, starter):
                print(f"player {self.players[i].name}, put your card> ")
                self.data.table[i] = self.players[i].provoke("play")
                print(f"player {self.players[i].name} played {self.data.table[i]}.")

            self.data.starter_player = self.decideRoundWinner()
            name = self.players[self.data.starter_player].name
            self.findScore(name)

            for i in range(len(self.data.table)):
                self.data.table[i] = None

            print()
            print(f"player {name} got the tricks of this round.")
            tm.sleep(1)
            print()
            print("scores: ")
            for name in self.data.scores:
                print(f"{name}: {self.data.scores[name]}")

    def findWinner(self):
        winner = self.players[self.data.starter_player].name
        score = self.data.scores

        for name in self.data.scores:
            if score[winner] > score[name]:
                winner = name

        for name in self.data.scores:
            if score[winner] == score[name] and winner != name:
                return None

        return winner

    def run(self):
        self.rules.display()
        self.distributeCards()
        self.exchangeCards()
        self.findStarterPlayer()
        print("--- prefect thus far ---")
        print("now we begin the game")
        print()
        self.askPlayers()
        print()
        print("--- well it is over ---")
        tm.sleep(1)
        winner = self.findWinner()
        print("and the winner is ...")
        tm.sleep(1)
        if winner is None:
            print("it is actually a tie. Noone won!")
        else:
            print(f"player {winner} won this game!!!!!!!")
            print(f"congrats to you player {winner}")
