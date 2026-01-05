import random as rd

from games.common.Character import Character
from games.common.GameCard import GameCard


class HeartsBot(Character):

    def __init__(self, name):
        super().__init__(name)

    def pickRandomCard(self):
        suits = []
        cards = self.gameData.cards[self.name]
        for suit in cards:
            if len(cards[suit]) != 0:
                suits.append(suit)

        suit = rd.choice(suits)
        rd.shuffle(cards[suit])
        return cards[suit].pop()

    def getCardsToExchange(self):
        """ To choose the exchange cards, we will
        first try to see if we have the queen of spade.
        then we will try the hearts, and finally if we still
        can pick more cards we will grab any random cards.
        """
        QUEEN_SPADE = GameCard("spade", "queen")

        exchange_cards = []
        cards = self.gameData.cards[self.name]

        # see of the spade of queen exist
        for i in range(len(cards["spade"])):
            card = cards["spade"][i]
            if card == QUEEN_SPADE:
                cards["spade"].pop(i)
                exchange_cards.append(card)
                break

        pop_list = []

        # see if there are any hearts
        if len(cards["heart"]) != 0:
            for i in range(len(cards["heart"])):
                card = cards["heart"][i]
                if len(exchange_cards) < 3:
                    pop_list.append(i)
                    exchange_cards.append(card)
                else:
                    break

        for pop_ in range(len(pop_list) - 1, -1, -1):
            cards["heart"].pop(pop_)

        while len(exchange_cards) < 3:
            exchange_cards.append(self.pickRandomCard())

        return exchange_cards

    def isTableEmpty(self):
        for item in self.gameData.table:
            if item is not None:
                return False
        return True

    def findSmallestCard(self, suit, player):
        cards = self.gameData.cards[player][suit]
        which = 0

        if len(cards) != 0:
            for i in range(len(cards)):
                if cards[which].rank > cards[i].rank:
                    which = i
            return which
        else:
            return -1

    def canPlayHeart(self):
        """ if at least one player has a heart
        card that is larger than the smallest heart
        card that we have and must play it, then
        it is the wisest to play heart.
        returns the index of the heart card to play.
        otherwise -1.
        """
        lowest_heart = self.findSmallestCard("heart", self.name)
        if lowest_heart != -1:
            rank = self.gameData.cards[self.name]["heart"][lowest_heart].rank
            for player in self.gameData.cards:
                s = self.findSmallestCard("heart", player)
                if s != -1:
                    sRank = self.gameData.cards[player]["heart"][s].rank
                    if sRank > s:
                        return lowest_heart
        return -1

    def canPlaySpadeQueen(self):
        """
        checks if we can play the spade queen as the
        start of the game.
        """
        cards = self.gameData[self.name]["spade"]

        if len(cards) != 0:
            found = -1

            for i in range(len(cards)):
                card = cards[i]
                if card == GameCard("spade", "queen"):
                    found = i
                    break

                if found != -1:
                    for player in self.gameData.cards:
                        c = self.gameData.cards[player]["spade"]
                        ind = self.findSmallestCard("spade", player)
                        if ind != -1:
                            rank = c[ind].rank
                            if rank > GameCard.RANKS["queen"]:
                                return found
        return -1

    def getPrioCard(self):
        """
        returns a random card. It first prioritizes clubs and
        diamonds. Then spade and then heart.
        """
        cards = self.gameData.cards[self.name]

        da = []

        for suit in ["diamond", "club"]:
            if len(cards[suit]) != 0:
                da.append(suit)

        if len(da) != 0:
            chosen = rd.choice(da)
            ind = self.findSmallestCard(chosen, self.name)
            return cards[chosen].pop(ind)
        else:
            ind = self.findSmallestCard("spade", self.name)
            if ind != -1:
                rank = cards[ind].rank
                if rank == GameCard.RANKS["queen"]:
                    if len(cards["heart"]) == 0:
                        return cards["spade"].pop(ind)
                    else:
                        ind = self.findSmallestCard("heart", self.name)
                        return cards["heart"].pop(ind)
            else:
                ind = self.findSmallestCard("heart", self.name)
                return cards["heart"].pop(ind)

    def getUnSuitCard(self):
        """
        In the case were we do not have the suit card,
        we should play a different card. It is best
        to play a queen spade, a heart, if possible.
        """

        cards = self.gameData.cards[self.name]

        # checking if we have queen of spade
        for i in range(len(cards["spade"])):
            card = cards["spade"][i]
            if card == GameCard("spade", "queen"):
                return cards["spade"].pop(i)

        # checking if we have a heart
        if len(cards["heart"]) != 0:
            rd.shuffle(cards["heart"])
            return cards["heart"].pop()

        # at the end just pick any random card
        da = []
        for suit in ["diamond", "club"]:
            if len(cards[suit]) != 0:
                da.append(suit)
        chosen = rd.choice(da)
        rd.shuffle(cards[chosen])
        return cards[chosen].pop()

    def choosePlayCard(self):
        if self.isTableEmpty():
            ans = self.canPlayHeart()
            if ans != -1:
                return self.gameData.cards[self.name]["heart"].pop(ans)
            ans = self.canPlaySpadeQueen()

            if ans != -1:
                return self.gameData.cards[self.name]["spade"].pop(ans)
            return self.getPrioCard()
        else:
            suit = GameCard.getKindName(self.gameData.
                                        table[self.gameData.start_player].kind)
            cards = self.gameData.cards[self.name]

            if len(cards[suit]) != 0:
                ind = self.findSmallestCard(suit, self.name)
                return cards[suit].pop(ind)
            else:
                return self.getUnSuitCard()

    def provoke(self, action):
        if action == "exchange":
            return self.getCardsToExchange()
        elif action == "play":
            return self.choosePlayCard()
