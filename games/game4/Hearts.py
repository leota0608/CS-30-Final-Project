import random as rd
import time as tm

from games.common.GameHandler import GameHandler
from HeartsGameData import HeartsGameData
from HeartsBot import HeartsBot
from HeartsHumanPlayer import HeartsHumanPlayer
from games.common.GameCard import *


class Hearts(GameHandler):
    def __init__(self, names):

        # initializing players
        self.players = [None, None, None, None]
        for i in range(3):
            self.players[i] = HeartsBot(names[i])
        self.players[3] = HeartsHumanPlayer(names[3])

        # initializing game data
        self.data = HeartsGameData()
        self.initGameData()

        super().__init__(self.players, self.data)

    def initGameData(self):
        # initializing cards
        for player in self.players:
            self.data.cards.update({player.name: dict()})
            self.data.scores.update({player.name: 0})
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

    def run(self):
        self.distributeCards()
        self.exchangeCards()
        self.findStarterPlayer()


h = Hearts(["Ali", "Arya", "Morteza", "Karim"])
h.run()


