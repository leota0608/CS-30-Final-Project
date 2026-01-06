from games.common.Character import Character
from games.common.GameCard import GameCard


class CPHumanPlayer(Character):

    def __init__(self, name):
        Character.__init__(self, name)

    def getTrump(self):

        trump = ""
        cards = self.gameData.cards[self.name]

        for kind in cards:
            for card in cards[kind]:
                print(f" - {card}")

        while True:
            for kind in GameCard.KINDS:
                print(f" - {kind}")

            trump = input("please choose your trump? ")
            if trump in GameCard.KINDS:
                for kind in cards:
                    for card in cards[kind]:
                        if trump == GameCard.getKindName(card.kind):
                            return trump
                print("trump must exist among your cards.")
            else:
                print("invalid answer. Trump must be a valid card type")

    def printCards(self):
        cards = self.gameData.cards[self.name]
        for kind in cards:
            print(f" - {kind}")
            if len(cards[kind]) != 0:
                for card in cards[kind]:
                    print(f"     - {card}")
            else:
                print("     None")

    def doesExist(self, current_card):
        cards = self.gameData.cards[self.name][GameCard.getKindName(current_card.kind)]
        for i in range(len(cards)):
            card = cards[i]
            if card == current_card:
                return i
        return -1

    def getCard(self):

        def isItACard(input_):
            if len(input_) == 2:
                if input_[0] in GameCard.KINDS:
                    if input_[1] in GameCard.RANKS:
                        return True
            return False

        guideline = "Note: first enter the kind followed by comma followed by rank.\n" \
                    "ex: Spade, One         Heart, King"
        self.printCards()

        print()
        print(guideline)
        print()

        while True:
            given = input("pick a card to put on the table? ").lower()
            given = given.replace(" ", "")

            given = given.split(',')

            # check if the given input represent a card
            if isItACard(given):
                current_card = GameCard(given[0], given[1])
                # does the card actually exist in the player's deck
                ans = self.doesExist(current_card)
                if ans != -1:
                    cards = self.gameData.cards[self.name]
                    # check if the chosen card comply to the game's
                    # rules
                    last_card = self.gameData.table[self.gameData.last_winner_ind]
                    if last_card is not None:
                        king_kind = GameCard.getKindName(last_card.kind)
                        # if the player has similar card to the
                        # the first player but the chosen card is
                        # different
                        if len(cards[king_kind]) != 0:
                            if given[0] != king_kind:
                                print("haven't you read the rules cheater??")
                                print(f"you cannot put a {given[0]} while you"
                                      f" have {king_kind}.")
                                print("ah hhh ....., repack again.")
                                continue
                        return cards[given[0]].pop(ans)
                    else:
                        return cards[given[0]].pop(ans)
                else:
                    print("the given card does not exist in your deck")
            else:
                print("Error: Invalid Input")
                print(guideline)

    def provoke(self, action):
        if action == "trump":
            if self.gameData.king.name == self.name:
                return self.getTrump()
        elif action == "pick":
            return self.getCard()
