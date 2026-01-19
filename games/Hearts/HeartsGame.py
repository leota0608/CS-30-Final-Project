###############################################################################
# Coder: Amir
# Last date modified: 1/14/2026
###############################################################################
""" Implements the game handler for game of hearts. HeartsGame 
game handler ensures that game goes in the correct flow, prints 
interactive messages and can report results and report the winner."""
###############################################################################
import random as rd
import time as tm

import games.common.score as score
from games.common.GameHandler import GameHandler
from games.Hearts.HeartsGameData import HeartsGameData
from games.Hearts.HeartsBot import HeartsBot
from games.Hearts.HeartsHumanPlayer import HeartsHumanPlayer
from games.common.GameCard import *
from games.teller.Teller import Teller
import games.common.Name as nm
from games.common.BodyPartsAnim import BodyPartsAnim


class HeartsGame(GameHandler):
    """ HeartsGame is GameHandler child class. We first
    ask the players to choose their exchange cards then
    we change and update each player deck in the game data.
    Then in each round we will ask players in order to draw
    their card.
    Note: Checking for the legality of a move is left
    to the Characters as it legality of the move is part the
    program logic to choose a move, and it has no other point than
    for testing.
    Then we update each player's score. Once the 13 rounds are over
    we will report the winner.

    There has been minor changes to laws of hearts notably:
    1 - Real hearts is played in four hands, here due to time
        constraints it is only played in one hand.
    2 - In actual hearts no one is allowed to play a heart before
        the first heart is played when someone did not have the suit.
        However, sometimes it takes a lot of rounds until we reach such
        a point and to make the game more interactive, it is omitted.
    """
    def __init__(self, user, money):
        """ user: it is an object of the Player class which contains
        all methods to modify the player. (Player)
            money: the amount of money to pay the player if they 
            won.(int)
        """
        # the actual user
        self.user = user
        self.result = None      # by default all games are draw
        # the money we are gambling on. The user gets this money
        # if they win
        self.money = money
        # animations
        self.anims = BodyPartsAnim(self.user)
        # initializing players
        self.players = [None, None, None, None]
        names = nm.select_name(self.user.name, 3)
        for i in range(3):
            self.players[i] = HeartsBot(names[i])
        self.players[3] = HeartsHumanPlayer(self.user.name)
        # initializing game data
        self.data = HeartsGameData()
        self.initGameData()
        # upload the roles
        self.rules = Teller("games/Hearts/rules.txt")
        # initialize the parent class.
        super().__init__(self.players, self.data, "hearts")

    def initGameData(self):
        """ Sets the entries in the game data according to the
        players.
        """
        # initializing cards
        # construct the structure of self.data.cards
        # it is represented as following.
        # {player name: {suit: [list of cards with that suit],
        #  ...}, ...}
        for player in self.players:
            self.data.cards.update({player.name: dict()})
            self.data.scores.update({player.name: 0})
            self.data.table.append(None)
            for kind in GameCard.KINDS:
                self.data.cards[player.name].update({kind: list()})

    def distributeCards(self):
        """ randomly shuffle cards and distribute them among
        all the players to fill up their decks.
        """
        deck = generateDeck()       # generate a ordered deck
        rd.shuffle(deck)
        # compute each player's number of cards.
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
        cards_: a list of cards.(list)
        name: which player. (ste)
        """
        # retrieve given player's cards.
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
                    # if the ith player had the spade
                    # of two they will start the game.
                    if card == SPADE_TWO:
                        self.data.starter_player = i
        # retrieve first player name.
        name = self.players[self.data.starter_player].name
        print(f"lucky you player, {name}.")
        print(f"you will start the game first.")
        tm.sleep(1)
        print()

    def exchangeCards(self):
        """ asks each player to choose their exchange cards and
        then changes with the player to the side.
        """
        print(" --- its time to exchange cards ---")
        cards_to_change = []
        for player in self.players:
            print(f"player {player.name} please pick "
                  "your three cards to exchange.")
            cards_to_change.append(player.provoke("exchange"))
            tm.sleep(1)
            print("thanks!")
        print("exchanging cards ...")
        tm.sleep(2)
        for i in range(len(self.players) - 2, -1, -1):
            prev = i + 1
            self.addCards(cards_to_change[prev], self.players[i].name)
        self.addCards(cards_to_change[0], \
                      self.players[len(self.players) - 1].name)
        print("cards had been exchanged")
        print()

    def decideRoundWinner(self):
        """
        decides the winner of the game by finding
        the player who played the highest rank with the
        same kind(suit) as the first player.
        Though as it is mentioned in the games, rules you win
        with the lowest rank!
        """
        starter = self.data.starter_player
        table = self.data.table
        # this suit is not in terms of string value
        suit = table[starter].kind
        rank = table[starter].rank
        winner = starter
        # choose the player who played the highest rank
        # in the table.
        for i in range(len(self.players)):
            if table[i].kind == suit:
                if table[i].rank > rank:
                    rank = table[i].rank
                    winner = i
        return winner

    def findScore(self, name):
        """ calculates a specific player's source.
        For every heart, they get a score of 1 and for
        queen of spade a score of 13.
        name: the given player.(str)
        """
        score = 0
        for card in self.data.table:
            if card.kind == GameCard.KINDS["heart"]:
                score += 1
            elif card == GameCard("spade", "queen"):
                score += 13
        self.data.scores[name] += score

    def askPlayers(self):
        """ asks player's four the next move until all the rounds
        are over. At the end of each round we display the scores.
        The majority of the time will be spent here in this function.
        """
        rounds = 52 // len(self.players)
        for round_ in range(rounds):
            print(f"------ round {round_} --------")
            # self.printPlayerCards()
            starter = self.data.starter_player
            # ask each player to draw their cards
            for i in range(starter, len(self.players)):
                print(f"player {self.players[i].name}, put your card> ")
                self.data.table[i] = self.players[i].provoke("play")
                print(f"player {self.players[i].name} played "
                      f"{self.data.table[i]}.")
            for i in range(0, starter):
                print(f"player {self.players[i].name}, put your card> ")
                self.data.table[i] = self.players[i].provoke("play")
                print(self.data.table[i])
                tm.sleep(2)
            # decide the round winner by computing the scores
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
            tm.sleep(1)

    def findWinner(self):
        """ The winner of the whole game is the one who has
        the least score. This is the twist of hearts! Score
        is negative points.
        """
        # choose any arbitrary player as the current winner
        winner = self.players[self.data.starter_player].name
        score = self.data.scores
        # check other players
        for name in self.data.scores:
            if score[winner] > score[name]:
                winner = name
        # if there are more two player with the same score
        # claim noone won.
        for name in self.data.scores:
            if score[winner] == score[name] and winner != name:
                return None
        return winner

    def run(self):
        """ run is the only function that is supposed to
        be called from any handler. It runs the game in the
        correct order.
        """
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
        # handle game results
        isTie = winner is None
        if winner != self.user.name or winner is None:
            self.result = False
        else:
            self.result = True
        score.updateScore(self.result, self.user, self.money, isTie)
        