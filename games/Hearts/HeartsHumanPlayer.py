import time as tm

from games.common.Character import Character
from games.common.GameCard import *


class HeartsHumanPlayer(Character):
    def __init__(self, name):
        super().__init__(name)

    def doesCardExist(self, c):
        cards = self.gameData.cards[self.name]
        for suit in cards:
            for i in range(len(cards[suit])):
                if c == cards[suit][i]:
                    return i
        return -1

    @staticmethod
    def isValidCard(suit, rank):
        if suit in GameCard.KINDS:
            if rank in GameCard.RANKS:
                return True
        return False

    def getCard(self,  print_guide=True):
        guideline = "Note: first enter the kind followed by comma followed by rank.\n" \
                    "ex: Spade, Two         Heart, King"

        if print_guide:
            print()
            print(guideline)
            print()

        while True:
            inp = input("pick a card> ").lower()
            inp = inp.replace(" ", "")
            inp = inp.split(",")

            if len(inp) == 2 and self.isValidCard(inp[0], inp[1]):
                current_card = GameCard(inp[0], inp[1])
                ans = self.doesCardExist(current_card)
                if ans != -1:
                    self.gameData.cards[self.name] \
                        [GameCard.getKindName(current_card.kind)].pop(ans)
                    return current_card
                else:
                    print("this card does not exist in your deck my friend.")
                    print("Try again")
                    print()
            else:
                print("Error: this card is invalid")
                print(guideline)
                print()

    def printCards(self):
        cards = self.gameData.cards[self.name]

        printDeck(cards)

    def chooseExchangeCards(self):
        exchange_cards = []

        print("choose three cards to change.")
        print()
        tm.sleep(1)
        self.printCards()
        print()

        for i in range(3):
            exchange_cards.append(self.getCard(i == 0))
        return exchange_cards

    def choosePlayingCard(self):

        print_guide = True

        self.printCards()
        print()

        while True:
            card = self.getCard(print_guide)

            suit_card = self.gameData.table[self.gameData.starter_player]

            # there is a suit in the game
            # card must match its suit
            if suit_card is not None:
                if suit_card.kind != card.kind:
                    suit_name = GameCard.getKindName(suit_card.kind)
                    if len(self.gameData.cards[self.name][suit_name]) != 0:
                        print("idiot, don't you know that your card must match the game suit")
                        print("try again, you cheater!")
                    else:
                        return card
                else:
                    return card
            else:
                return card

            print_guide = False

    def provoke(self, action):
        if action == "exchange":
            return self.chooseExchangeCards()
        elif action == "play":
            return self.choosePlayingCard()
