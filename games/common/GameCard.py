

class GameCard:
    KINDS = {"club": 0, "spade": 1, "heart": 2, "diamond": 3}
    RANKS = {"two": 0, "three": 1, "four": 2, "five": 3,
             "six": 4, "seven": 5, "eight": 6, "nine": 7, "ten": 8,
             "jack": 9, "queen": 10, "king": 11, "ace": 12}

    PRINT_CARD = """
┌─────┐
│{}  {}│
│  {}  │
│{}  {}│
└─────┘
"""

    def __init__(self, kind, rank):
        kind_t = type(kind)
        rank_t = type(rank)

        if kind_t == str and rank_t == str:
            self.kind = self.KINDS[kind]
            self.rank = self.RANKS[rank]
        elif kind_t == int and rank_t == int:
            self.kind = kind
            self.rank = rank
        else:
            raise TypeError(f"unsupported data types provided for class"
                            f" {self.__class__.__name__}")

    @staticmethod
    def getCardRankForPrint(rank):
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
        if suit == GameCard.KINDS["club"]:
            return '♧'
        elif suit == GameCard.KINDS["heart"]:
            return '♡'
        elif suit == GameCard.KINDS["diamond"]:
            return '♢'
        elif suit == GameCard.KINDS["spade"]:
            return '♠'

    def constructPrintCard(self):
        rank = self.getCardRankForPrint(self.rank)
        suit = self.getCardSuitForPrint(self.kind)

        rank1 = rank
        rank2 = rank

        if len(rank) == 1:
            rank1 = rank + " "
            rank2 = " " + rank

        return self.PRINT_CARD.format(rank1, suit, suit, suit, rank2)

    @staticmethod
    def getKindName(kind):
        for card_kind in GameCard.KINDS:
            if GameCard.KINDS[card_kind] == kind:
                return card_kind
        return None

    @staticmethod
    def getRankName(rank):
        for card_rank in GameCard.RANKS:
            if GameCard.RANKS[card_rank] == rank:
                return card_rank
        return None

    def getName(self):
        return GameCard.getKindName(self.kind), GameCard.getRankName(self.rank)

    def similarKind(self, other):
        return self.rank == other.rank

    def __str__(self):
        return self.constructPrintCard()

    def __eq__(self, other):
        return other.kind == self.kind and \
               other.rank == self.rank

    def __gt__(self, other):
        """ Important: only checks if self has a greater rank.
        Make sure to check any other prerequisites.
        """
        return self.rank > other.rank

    def __lt__(self, other):
        return not self.__gt__(other)

    def __ge__(self, other):
        return self.__gt__(other) or self.__eq__(other)

    def __le__(self, other):
        return not self.__ge__(other)


def generateDeck():
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
    """
    lines = card_str.splitlines()
    max_line_len = max(len(line) for line in lines)
    formatted_lines = [line.ljust(max_line_len) for line in lines]
    return formatted_lines


def printDeck(deck, row_length=7):
    """
    deck is a dict of suits -> list of cards
    Each card prints as multi-line ASCII art
    """

    for suit in deck:
        symbol = GameCard.getCardSuitForPrint(GameCard.KINDS[suit])
        print(f" - {suit}({symbol}):")

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
