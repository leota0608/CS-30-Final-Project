###############################################################################
# Coder: Amir
# Last date modified: 1/14/2026
###############################################################################
""" CourtPieceGame is a class that implements the correct sequence at
the game of court piece is played. It is also responsible for reporting the
winner of the game as well as reporting the results and doing any necessary
damage to the player.
"""
###############################################################################
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
    """ CourtPieceGame inherit from the game handler class
    in the commons. It defines the run() function which allows
    the game to be started with a single method.

    First this class would shuffle the cards thoroughly, and
    give one card to each player. Until one of the players get
    an ace it continues. Now that we know the king, we choose the
    trump and immediately after the game starts.
    """
    DOUBLE_PLAY = 2
    TRIPLE_PLAY = 3
    QUADRUPLE_PLAY = 4

    def __init__(self, user, money):
        """ user: an object of the Player class. It stores
            player info and related methods.(Player)
            money: The amount of money we would pay to the user
            if they won.(int)
        """
        # set the pre-mode
        self.mode = self.TRIPLE_PLAY
        # create the animations objects
        self.anims = BodyPartsAnim(user)
        # store the actual user
        self.user = user
        self.result = None  # game result is by default draw
        self.money = money
        self.players = []
        # select self.mode - 1 names that does not include
        # the real player's name. These are the bot names.
        names = nm.select_name(self.user.name, self.mode - 1)
        # Construct bot objects
        for i in range(self.mode - 1):
            self.players.append(CPBot(names[i]))
        self.players.append(CPHumanPlayer(self.user.name))
        # calculate number of rounds
        # the formula is 2 (4 - number of players) + 7
        self.rounds = 2 * (4 - self.mode) + 7
        self.data = CPGameData()
        self.createCardEntries()
        # rules
        self.rules = Teller("games/CourtPiece/rules.txt")
        GameHandler.__init__(self, self.players, self.data, "court piece")

    def createCardEntries(self):
        """ Sets up the card entries for each player
        and sets each player score to 0 at the start of the
        game.
        """
        for player in self.players:
            self.data.cards[player.name] = dict()
            self.data.scores.update({player.name: 0})
            # the game cards follow the following structure:
            # {player name: {suit: [list of cards with that suit], 
            # ...}, ...}
            for kind in GameCard.KINDS:
                self.data.cards[player.name].update({kind: []})
        self.data.table = [None] * len(self.players)

    def decideKing(self):
        """ Shuffles a full deck of cards and give each player
        a card. The player who got an ace will be the king.
        """
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
                    # this player is now the king
                    print(f"awsome player {player.name}.")
                    print(f"you are the king of this game.")
                    self.data.king = player
                    self.data.last_winner_ind = i
                    deciding_king = False
                    break
                tm.sleep(1)

    def decideTrump(self, deck):
        """ We give the king 5 cards, and they will choose
        a specific suit as the trump of the game.
        The chosen trump will remain the trump to the end.
        deck: the official deck of the game. (list)
        """
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
        """ distributes the cards among all the players out of
        shuffled deck. The deck might contain some card depending
        on the mode of the game.(number of players)
        deck: a list that represents the official deck of cards.(list)
        """
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
        """ Asks the players in a given round.
        It asks all the players give their cards.
        round: which round of court piece are we in.(int)
        """
        print()
        print(f" --- round {round} begin ---")
        print()

        def ask(i_):
            """ provokes a player to pick a card.
            It places the card on the table.
            Briefly asks the player to play a card.
            i_: which player index. (int)
            """
            name = self.players[i_].name
            print(f"player {name} put your card.")
            card = self.players[i_].provoke("pick")
            self.data.table[i_] = card
            print(card)
            tm.sleep(2)

        # the last player starts the round
        start = self.data.last_winner_ind
        # as the previous winner
        ask(start)
        winner = self.data.last_winner_ind
        kind = self.data.table[start].kind
        rank = self.data.table[start].rank

        def update(i_):
            """ checks if the currently drawn
            card can be a winner.
            i_: the index of previously playing player.
            """
            nonlocal winner, kind, rank
            # set the suit and rank of
            # the previous card to make access easier.
            put_kind = self.data.table[i_].kind
            put_rank = self.data.table[i_].rank
            if put_kind == kind:
                # if suits match and that they played a higher
                # rank they are the next winner.
                if put_rank > rank:
                    winner = i_
                    rank = put_rank
            elif put_kind == GameCard.KINDS[self.data.trump]:
                # if they played a trump card, they are winner
                # always, unless another player has played higher
                # rank trump.
                if kind != put_kind:
                    kind = put_kind
                    rank = put_rank
                    winner = i_
                elif put_rank > rank:
                    rank = put_rank
                    winner = i_

        # ask the players and update winner
        for i in range(start + 1, len(self.players)):
            ask(i)
            update(i)
        for i in range(0, start):
            ask(i)
            update(i)

        # reset the table
        for i in range(len(self.data.table)):
            self.data.table[i] = None
        # set the new winner
        self.data.last_winner_ind = winner
        name = self.players[winner].name
        self.data.scores[name] += 1
        # announce this round winner
        print()
        print(f"yay, player {name} won this round!!")
        print()
        print("results thus far are:")
        for name in self.data.scores:
            print(f"{name}: {self.data.scores[name]}")
        # self.printPlayerCards()
        tm.sleep(2)

    def getWinner(self):
        """ finds the player with maximum score and returns it
        as the winner of the game.
        """
        winner = ""
        max_score = 0
        for name in self.data.scores:
            if self.data.scores[name] > max_score:
                max_score = self.data.scores[name]
                winner = name
        return winner

    def run(self):
        """ It is the only function supposed to be called from outside.
        It runs the game in the correct order as it is supposed to.
        """
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

        isTie = winner is None

        if winner != self.user.name or winner is None:
            self.result = False
        else:
            self.result = True

        score.updateScore(self.result, self.user, self.money, isTie)
