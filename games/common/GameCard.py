

class GameCard:
    KINDS = {"club": 0, "spade": 1, "heart": 2, "diamond": 3}
    RANKS = {"two": 0, "three": 1, "four": 2, "five": 3,
             "six": 4, "seven": 5, "eight": 6, "nine": 7, "ten": 8,
             "jack": 9, "queen": 10, "king": 11, "ace": 12}

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
        name = self.getName()
        return f"card({name[0]}, {name[1]})"

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
