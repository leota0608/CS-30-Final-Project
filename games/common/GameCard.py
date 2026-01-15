#######################################################################
# Coder: Amir
# Last date modified: 1/14/2026
#######################################################################
''' This module defines a class for standard playing cards. This class 
standardize playing cards by facilitating comparison of different cards
with different ranks. It also allows you to print the cards in a nice
rectangular manner.
Cards are internally represented using code numbers to facilitate 
comparison of different ranks. However methods for transition from
code number to string is also provided.
'''
#######################################################################
class GameCard:
    """ Internally represents a card game. The card is transformed
    to code according to the static dictionaries KINDS and RANKS.
    Operators of __eq__, __gt__, __lt__, __le___ and __ge__ are overloaded
    and they allow for comparison of the cards.
    __str__ function would print a card in a rectangular box much
    like a real card once provoked.
    """
    KINDS = {"club": 0, "spade": 1, "heart": 2, "diamond": 3}
    RANKS = {"two": 0, "three": 1, "four": 2, "five": 3,
             "six": 4, "seven": 5, "eight": 6, "nine": 7, "ten": 8,
             "jack": 9, "queen": 10, "king": 11, "ace": 12}
    # print card template
    PRINT_CARD = """
┌─────┐
│{}  {}│
│  {}  │
│{}  {}│
└─────┘
"""

    def __init__(self, kind, rank):
        """
        kind: the type of card also known as suit.(str or int)
        rank: the rank of card. (str, int)
        """
        kind_t = type(kind)
        rank_t = type(rank)
        # loading from string
        if kind_t == str and rank_t == str:
            self.kind = self.KINDS[kind]
            self.rank = self.RANKS[rank]
        # loading from standard integral codes
        elif kind_t == int and rank_t == int:
            self.kind = kind
            self.rank = rank
        else:
            raise TypeError(f"unsupported data types provided for class"
                            f" {self.__class__.__name__}")

    @staticmethod
    def getCardRankForPrint(rank):
        """ returns an string that represents the rank.
        rank: integral code for a card.(int)
        """
        if 0 <= rank <= 8:
            return str(rank + 2)
        elif rank == 9:
            return "J"
        elif rank == 10:
            return "Q"
        elif rank == 11:
            return "K"
        elif rank == 12:
            return "A"

    @staticmethod
    def getCardSuitForPrint(suit):
        """Returns the icon for each type of
        card.
        suit: integral code of a suit.(int)
        """
        if suit == GameCard.KINDS["club"]:
            return '♧'
        elif suit == GameCard.KINDS["heart"]:
            return '♡'
        elif suit == GameCard.KINDS["diamond"]:
            return '♢'
        elif suit == GameCard.KINDS["spade"]:
            return '♠'

    def constructPrintCard(self):
        """ Creates the current card for printing.
        It formats them into the static template that
        we have.
        """
        # prepare the card info
        rank = self.getCardRankForPrint(self.rank)
        suit = self.getCardSuitForPrint(self.kind)
        rank1 = rank    # printed in the top left of the card
        rank2 = rank    # printed in the bottom right of the card
        if len(rank) == 1:
            rank1 = rank + " "
            rank2 = " " + rank
        return self.PRINT_CARD.format(rank1, suit, suit, suit, rank2)

    @staticmethod
    def getKindName(kind):
        """ returns the suit(kind) name given the integral
        code.
        kind: integral code for a suit.(int)
        """
        for card_kind in GameCard.KINDS:
            if GameCard.KINDS[card_kind] == kind:
                return card_kind
        return None

    @staticmethod
    def getRankName(rank):
        """ returns the rank name given the integral
        code.
        rank: integral code for a specific rank.(int)
        """
        for card_rank in GameCard.RANKS:
            if GameCard.RANKS[card_rank] == rank:
                return card_rank
        return None

    def getName(self):
        """ Returns a tuple pairing the string suit name and
        rank name of the current card.
        """
        return GameCard.getKindName(self.kind), GameCard.getRankName(self.rank)

    def similarKind(self, other):
        """ checks of another card is of the same suit as
        the current card.
        other: another card. (GameCard)
        """
        return self.rank == other.rank

    def __str__(self):
        """ constructs and returns a card.
        """
        return self.constructPrintCard()

    def __eq__(self, other):
        """ check if another card is the same as the current
        card. You can use the operator == to compare.
        other: another game card. (GameCard)
        """
        return other.kind == self.kind and \
            other.rank == self.rank

    def __gt__(self, other):
        """ check if we have greater rank than another player.
        You can use the operator > to compare.
        other: another game card. (GameCard)
        """
        return self.rank > other.rank

    def __lt__(self, other):
        """ check if we have smaller rank than another card.
        other: another game card. (GameCard)
        """
        return not self.__gt__(other)

    def __ge__(self, other):
        """ check if we have a greater or equal to rank
        than another player.
        other: another game card. (GameCard)
        """
        return self.__gt__(other) or self.__eq__(other)

    def __le__(self, other):
        """ check if we have a smaller or equal to rank
        than another player.
        other: another game card. (GameCard)
        """
        return not self.__ge__(other)


def generateDeck():
    """ Generates an ordered 52 card deck.
    """
    cards = []
    for kind in range(0, 4):
        for rank in range(0, 13):
            cards.append(GameCard(kind, rank))
    return cards


def formatCard(card_str):
    """
    Takes the ASCII card string and ensures that ranks
    inside the card are properly aligned (handles '10').
    Returns a list of lines, all same width.
    card_str: the string that represents a card. (str)
    """
    lines = card_str.splitlines()
    max_line_len = max(len(line) for line in lines)
    formatted_lines = [line.ljust(max_line_len) for line in lines]
    return formatted_lines


def printDeck(deck, row_length=7):
    """
    deck is a dict of {suits: list of cards}
    Each card prints as multi-line ASCII character.
    deck: ordered dictionary of cards. (dict)
    row_length: max length in a row. (int)
    """
    for suit in deck:
        symbol = GameCard.getCardSuitForPrint(GameCard.KINDS[suit])
        print(f" - {suit}({symbol}):")
        # cards of a specific suit
        cards = deck[suit]
        if not cards:
            print("None")
            continue
        # Convert each card to a list of lines
        card_lines = [str(card).splitlines() for card in cards]
        card_height = len(card_lines[0])
        # Process cards in chunks of row_length
        for i in range(0, len(card_lines), row_length):
            chunk = card_lines[i:i + row_length]
            # Print cards side-by-side line by line
            for line_idx in range(card_height):
                for card in chunk:
                    print(card[line_idx], end="  ")
                print()


def printCardList(cards, row_length=2):
    """ prints a given list of cards in rows of 
    maximum length row_length.
    cards: a list of cards. (cards)
    row_length: the length of each row. (int)
    """
    # Convert each card to a list of lines
    card_lines = [str(card).splitlines() for card in cards]
    card_height = len(card_lines[0])
    # Process cards in chunks of row_length
    for i in range(0, len(card_lines), row_length):
        chunk = card_lines[i:i + row_length]
        # Print cards side-by-side line by line
        for line_idx in range(card_height):
            for card in chunk:
                print(card[line_idx], end="  ")
            print()
