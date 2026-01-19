###############################################################################
# Coder: Amir
# Last date modified: 1/14/2026
###############################################################################
""" Creates an interface between the game handler and the actual user.
By inheriting from the Character class, we make sure that character 
logic is separate from game handler, so later we can make this game to 
have multiple real players if we wish to."""
###############################################################################
import time as tm

from games.common.Character import Character
from games.common.GameCard import *


class HeartsHumanPlayer(Character):
    """ HeartsHumanPlayer defines all the logic needed to
    interact with the actual user. It asks the user to enter its 3
    change cards in the game, exchange phase.
    Then at every call to provoke with "play", it would ask the user
    to choose their card. Interactive guidance is developed to let the
    user know if their choice is illegal and that what they should do.
    """
    def __init__(self, name):
        """ name is the name of the player. It is needed
        as unique identifier of this player.
        """
        super().__init__(name)

    def doesCardExist(self, c):
        """ Checks of a given card c exists in the players
        deck.
        c: any arbitrary card. (GameCard)
        """
        # enumerate all the cards and check
        cards = self.gameData.cards[self.name]
        for suit in cards:
            for i in range(len(cards[suit])):
                if c == cards[suit][i]:
                    # return the index
                    return i
        # return -1 if the card does not exist
        return -1

    @staticmethod
    def isValidCard(suit, rank):
        """ checks of a given pair of suit and rank represents a
        real card.
        """
        if suit in GameCard.KINDS:
            if rank in GameCard.RANKS:
                return True
        return False

    def getCard(self, print_guide=True):
        """ Asks the user to play a card.
        print_guide: if true a simple guide about hoe input works
        is displayed at the beginning.
        """
        guideline = "Note: first enter the kind followed by comma " \
                    "followed by rank.\n" \
                    "ex: Spade, Two         Heart, King"
        if print_guide:
            print()
            print(guideline)
            print()
        while True:
            inp = input("pick a card> ").lower()
            inp = inp.replace(" ", "")
            inp = inp.split(",")
            # if input has two elements and those elements are
            # one suit and the other rank construct the card
            # and do the other pre-checks
            if len(inp) == 2 and self.isValidCard(inp[0], inp[1]):
                current_card = GameCard(inp[0], inp[1])
                # checking card existance in the deck
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
        """ prints the current player's deck in rows for.
        """
        cards = self.gameData.cards[self.name]
        printDeck(cards)

    def chooseExchangeCards(self):
        """ Asks the user to pick three exchange cards for
        the game
        """
        # list of exchange cards
        exchange_cards = []
        print("choose three cards to change.")
        print()
        tm.sleep(1)
        self.printCards()
        print()
        for i in range(3):
            # cards are automatically removed once chosen at
            # getCard.
            # i == 0 ensures that the guideline only appears once.
            exchange_cards.append(self.getCard(i == 0))
        return exchange_cards

    def choosePlayingCard(self):
        """ Asks the user to choose their play card.
        It forces the user to play suit when they have it.
        Otherwise, if they do not have suit they are allowed to play
        other card.
        """
        print_guide = True
        self.printCards()   # print cards only once
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
                        print("idiot, don't you know that your " \
                        "card must match the game suit")
                        print("try again, you cheater!")
                    else:
                        return card
                else:
                    # suit and chosen card match
                    return card
            else:
                # no suit in the game
                return card
            # reset it so guideline is not printed over and over!
            print_guide = False

    def provoke(self, action):
        """ it is the only function that is supposed to be called
        by game handler directly. It would return the response based
        on the request action.
        action: if "exchange" return a list of cards for change. if
                "play" returns the next playing card.(str)
        """
        if action == "exchange":
            return self.chooseExchangeCards()
        elif action == "play":
            return self.choosePlayingCard()
