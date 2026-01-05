import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from games.common.Character import Character
from games.common.GameCard import GameCard
import random as rd


class CPBot(Character):
    def __init__(self, name):
        Character.__init__(self, name)

    def chooseTrump(self):
        """
        to pick a good trump we count each kind
        of card that we have, and we choose the kind that
        we have the most of. For example if our cards are
        Card(Heart, Ace), Card(Spade, One), Card(Heart, Two),
        Card(Spade, King), Card(Heart, Queen), then heart
        is the trump.
        """
        cards = self.gameData.cards[self.name]
        trump = rd.choice(list(GameCard.KINDS.keys()))
        count = 0

        for kind in cards:
            if len(cards[kind]) > count:
                trump = kind
                count = len(cards[kind])

        return trump

    def isTableEmpty(self):
        for item in self.gameData.table:
            if item is not None:
                return False
        return True

    def getRandomCard(self):
        cards = self.gameData.cards[self.name]
        kinds = []
        for kind in cards:
            if len(cards[kind]) != 0:
                kinds.append(kind)
        chosen_kind = rd.choice(kinds)
        rd.shuffle(cards[chosen_kind])
        return cards[chosen_kind].pop()

    def findLargestRank(self, kind):
        cards = self.gameData.cards[self.name][kind]
        which = 0
        for i in range(len(cards)):
            if cards[i].rank > cards[which].rank:
                which = i
        return which

    def findSmallestRank(self, kind):
        cards = self.gameData.cards[self.name][kind]
        which = 0
        for i in range(len(cards)):
            if cards[i].rank < cards[which].rank:
                which = i
        return which

    def provoke(self, action):
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
