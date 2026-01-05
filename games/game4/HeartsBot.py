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

    def provoke(self, action):
        if action == "exchange":
            return self.getCardsToExchange()
