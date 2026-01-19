###############################################################################
# Coder: Amir
# Last date modified: 1/14/2026
###############################################################################
""" Creates the logic for a computer player that plays Hearts. The class
is wrapped around with the outlined design structure of Character class.
"""
###############################################################################
from games.common.Character import Character
from games.common.GameCard import GameCard
import random as rd


class CPBot(Character):
    """ CPBot short for Court Piece Bot defines the logic for a 
    computer player in the game of Court Piece. Each Computer Player 
    operates independently which is the advantage of the Character/Game
    Handler design.
    Here is the flow chart sudo code for how the algorithm of CPBot 
    works.

    # Choosing Trump:
    - if the current Bot the king, choose the suit that you have 
    the most as your trump.
    # Playing:
    - if we are the first player of the game, then return any random 
    card back.
    - otherwise if we are a middle player:
        - first determine the suit or king kind of the game.
        - if we have cards of this type then find the maximum and 
        minimum ranks.
            - if the max card is higher than one of cards placed 
            already on the table draw the max card.
            - otherwise use the min card to avoid losing the max 
            card.
        - otherwise, we look into using a trump. If we have a trump
          card, pick the smallest trump card that we have.
        - or else, just pick any random card!
    """

    def __init__(self, name):
        """ name: the name of the player used as their identifier.(str)
        """
        Character.__init__(self, name)

    def chooseTrump(self):
        """ to pick a good trump we count each kind
        of card that we have, and we choose the kind that
        we have the most of. For example if our cards are
        Card(Heart, Ace), Card(Spade, One), Card(Heart, Two),
        Card(Spade, King), Card(Heart, Queen), then heart
        is the trump.
        """
        cards = self.gameData.cards[self.name]
        trump = rd.choice(list(GameCard.KINDS.keys()))
        count = 0
        # choose the suit/kind that we have the most of.
        for kind in cards:
            if len(cards[kind]) > count:
                trump = kind
                count = len(cards[kind])
        return trump

    def isTableEmpty(self):
        """ checks if the table is full or empty
        which directly implies of we are first player
        or a middle player.
        """
        for item in self.gameData.table:
            if item is not None:
                return False
        return True

    def getRandomCard(self):
        """ returns any random card back to the user.
        This function is most often used as a tie-breaker
        when no better option exists.
        """
        # retrieve current player's cards.
        cards = self.gameData.cards[self.name]
        # create a list of kinds also known as suit.
        kinds = []
        for kind in cards:
            if len(cards[kind]) != 0:
                kinds.append(kind)
        # pick the random card.
        chosen_kind = rd.choice(kinds)
        rd.shuffle(cards[chosen_kind])
        return cards[chosen_kind].pop()

    def findLargestRank(self, kind):
        """ returns the largest rank of a specific kind of card.
        Note: ensure that there cards of type kind.
        kind: kind/suit of that we want it's max rank. (str)
        """
        cards = self.gameData.cards[self.name][kind]
        which = 0   # index of the max card
        for i in range(len(cards)):
            if cards[i].rank > cards[which].rank:
                which = i
        return which

    def findSmallestRank(self, kind):
        """ returns the lowest rank of a specific kind of card.
        Note: ensure that there cards of type kind.
        kind: kind/suit of that we want it's min rank. (str)
        """
        cards = self.gameData.cards[self.name][kind]
        which = 0
        for i in range(len(cards)):
            if cards[i].rank < cards[which].rank:
                which = i
        return which

    def provoke(self, action):
        """ the only function called by game handler.
        If action is set to trump, the player will return
        its trump choice.
        If action set to pick, we are in the middle of game
        and the player returns its chosen card to be put on
        th table.
        action: It is either "trump" or "pick".(str)
        """
        # if we are the king, and we are asked
        # to choose the trump.
        if action == "trump":
            if self.gameData.king.name == self.name:
                return self.chooseTrump()
        elif action == "pick":
            # we begin the game.
            # choose any random card
            if self.isTableEmpty():
                return self.getRandomCard()
            else:
                king_kind = GameCard.getKindName(self.gameData.
                                                 table[self.gameData.
                                                 last_winner_ind].kind)
                cards = self.gameData.cards[self.name]
                trump = self.gameData.trump
                # we have several cards of the kind king
                # kind(the starting card of the round).
                # we would put the largest of such rank.
                # if a player has placed a higher rank,
                # then we put the smallest card.
                if len(cards[king_kind]) != 0:
                    c = cards[king_kind]
                    largest_i = self.findLargestRank(king_kind)
                    smallest_i = self.findSmallestRank(king_kind)
                    # print(self.name)
                    # print(c[largest_i])
                    # print(c[smallest_i])
                    for card in self.gameData.table:
                        if card is not None:
                            if card.kind == GameCard.KINDS[king_kind]:
                                if c[largest_i].rank < card.rank:
                                    return c.pop(smallest_i)
                            elif card.kind == GameCard.KINDS[trump]:
                                return c.pop(smallest_i)
                    return c.pop(largest_i)
                else:
                    # if we do not have king kind, but
                    # we have cards of type trump then we
                    # use trump to maximize wining chance.
                    if len(cards[trump]) != 0:
                        smallest_i = self.findSmallestRank(trump)
                        return cards[trump].pop(smallest_i)
                    else:
                        return self.getRandomCard()
