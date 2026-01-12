import random as rd
import time as tm

import games.common.score as score
from games.teller.Teller import Teller
from games.common.GameHandler import GameHandler
from games.CourtPiece.CPGameData import CPGameData
from games.CourtPiece.CPBot import CPBot
from games.CourtPiece.CPHumanPlayer import CPHumanPlayer
from games.common.GameCard import *
import games.common.Name as nm
from games.common.BodyPartsAnim import BodyPartsAnim

class CourtPieceGame(GameHandler):
    DOUBLE_PLAY = 2
    TRIPLE_PLAY = 3
    QUADRUPLE_PLAY = 4

    def __init__(self, user, money):

        # set the premode
        self.mode = self.QUADRUPLE_PLAY
        self.anims = BodyPartsAnim(user)
        self.user = user
        self.result = None
        self.money = money

        self.players = []
        names = nm.select_name(self.user.name, self.mode - 1)
        for i in range(self.mode - 1):
            self.players.append(CPBot(names[i]))
        self.players.append(CPHumanPlayer(self.user.name))

        self.rounds = 2 * (4 - self.mode) + 7
        self.data = CPGameData()
        self.createCardEntries()
        self.rules = Teller("games/CourtPiece/rules.txt")
        GameHandler.__init__(self, self.players, self.data, "court piece")

    def createCardEntries(self):
        for player in self.players:
            self.data.cards[player.name] = dict()
            self.data.scores.update({player.name: 0})
            for kind in GameCard.KINDS:
                self.data.cards[player.name].update({kind: []})
        self.data.table = [None] * len(self.players)

    def decideKing(self):
        print("--- we begin our game by deciding the king ---")
        deck = generateDeck()
        rd.shuffle(deck)
        print("-- shuffling, shuffling, shuffling ---")
        tm.sleep(2)
        deciding_king = True
        while deciding_king:
            for i in range(len(self.players)):
                player = self.players[i]
                print(f"{player.name}: ")
                chosen = deck.pop()
                print(chosen)
                if chosen.rank == GameCard.RANKS["ace"]:
                    print(f"awsome player {player.name}.")
                    print(f"you are the king of this game.")
                    self.data.king = player
                    self.data.last_winner_ind = i
                    deciding_king = False
                    break
                tm.sleep(1)

    def decideTrump(self, deck):
        print("--- deciding trump ---")

        king_name = self.data.king.name

        # giving 5 cards to the king and everyone else
        for i in range(5):
            # put cards in order with their kind
            # this makes searching and printing easier
            # in the future.
            for player in self.players:
                chosen = deck.pop()
                kind = GameCard.getKindName(chosen.kind)
                self.data.cards[player.name][kind].append(chosen)

        print(f"player {king_name}, choose your trump ")
        # call the player to tell us its trump.
        self.data.trump = self.data.king.provoke("trump")

        print(f"the trump is {self.data.trump}")

    def distributeCards(self, deck):
        count = len(deck) // len(self.players)

        for player in self.players:
            cards = self.data.cards[player.name]
            for i in range(count):
                chosen = deck.pop()
                cards[GameCard.getKindName(chosen.kind)].append(chosen)
        print("...")
        tm.sleep(1)
        print(f"everyone now has {count + 5} fresh cards!")
        print(f"do not reveal your cards ...")

    def askPlayers(self, round):
        print()
        print(f" --- round {round} begin ---")
        print()

        def ask(i_):
            name = self.players[i_].name
            print(f"player {name} put your card.")
            card = self.players[i_].provoke("pick")
            self.data.table[i_] = card
            print(card)
            tm.sleep(2)

        start = self.data.last_winner_ind
        # as the previous winner
        ask(start)
        winner = self.data.last_winner_ind
        kind = self.data.table[start].kind
        rank = self.data.table[start].rank

        def update(i_):
            nonlocal winner, kind, rank
            put_kind = self.data.table[i_].kind
            put_rank = self.data.table[i_].rank
            if put_kind == kind:
                if put_rank > rank:
                    winner = i_
                    rank = put_rank

            elif put_kind == GameCard.KINDS[self.data.trump]:
                if kind != put_kind:
                    kind = put_kind
                    rank = put_rank
                    winner = i_
                elif put_rank > rank:
                    rank = put_rank
                    winner = i_

        for i in range(start + 1, len(self.players)):
            ask(i)
            update(i)

        for i in range(0, start):
            ask(i)
            update(i)

        # reset the table
        for i in range(len(self.data.table)):
            self.data.table[i] = None
        self.data.last_winner_ind = winner
        name = self.players[winner].name
        self.data.scores[name] += 1
        print()
        print(f"yay, player {name} won this round!!")
        print()
        print("results thus far are:")
        for name in self.data.scores:
            print(f"{name}: {self.data.scores[name]}")
        # self.printPlayerCards()

    def printPlayerCards(self):
        for player in self.data.cards:
            print(player)
            for kind in self.data.cards[player]:
                for card in self.data.cards[player][kind]:
                    print(card)

    def getWinner(self):
        winner = ""
        max_score = 0
        for name in self.data.scores:
            if self.data.scores[name] > max_score:
                max_score = self.data.scores[name]
                winner = name
        return winner

    def run(self):
        self.rules.display()
        self.decideKing()
        distribution_deck = generateDeck()
        rd.shuffle(distribution_deck)
        self.decideTrump(distribution_deck)
        print()
        tm.sleep(2)
        print(" -- perfect thus far -- ")
        print()
        print("Now we get to the most interesting part ...")
        print("distributing the cards !! yay")
        self.distributeCards(distribution_deck)
        # self.printPlayerCards()
        print()
        print("...")
        tm.sleep(3)
        print("let's        B E G I N!!!! GOOOOOO")
        print(f"we will play {self.rounds}!")
        print()
        for i in range(self.rounds):
            self.askPlayers(i)
        print()
        print("and the the winner is ...")
        tm.sleep(2)
        winner = self.getWinner()
        if winner != "":
            print(f"--------- No Body Except Player {winner} --------")
        else:
            print(f"nobody actually won, it was a tie.")

        isTie = winner == None

        if winner != self.user.name or winner == None:
            self.result = False
        else:
            self.result = True
        
        score.updateScore(self.result, self.user, self.money, isTie)


