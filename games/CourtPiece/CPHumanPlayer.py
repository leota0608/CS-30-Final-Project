###############################################################################
# Coder: Amir
# Last date modified: 1/14/2026
###############################################################################
""" Creates an interface between the game handler and the actual user.
By inheriting from the Character class, we make sure that character logic
is separate from game handler, so later we can make this game to have multiple
real players if we wish to."""
###############################################################################
from games.common.Character import Character
from games.common.GameCard import *


class CPHumanPlayer(Character):
    """ CPHumanPlayer shortened for Court Piece Human Player 
    defines all the logic needed to interact with the actual player.
    First it will ask the user to give us the trump if the user was 
    chosen as the king. Then the rest of the game is about asking the 
    player to draw a card from their deck to play.
    Here are the conditions that must be true about the player's chosen
    cards:
    - If they have the suit they must play it.
    - If they do not they can either play a trump or any other card
      depending on availability.
    """

    def __init__(self, name):
        """ name: It is the name of the actual player.(str)
        """
        Character.__init__(self, name)

    def getTrump(self):
        """ Asks the user to give the trump out
        of the five cards given to them by game handler.
        Cards are printed, and they choose one of the present
        suits in the cards.
        """
        trump = ""
        # retrieve current player's cards.
        cards = self.gameData.cards[self.name]
        # print player's available five cards.
        for kind in cards:
            for card in cards[kind]:
                print(f" - {card}")
        while True:
            # print all the kinds or suits.
            for kind in GameCard.KINDS:
                print(f" - {kind}")
            trump = input("please choose your trump? ")
            # check if the trump exist in deck and is
            # not misspelled.
            if trump in GameCard.KINDS:
                for kind in cards:
                    for card in cards[kind]:
                        if trump == GameCard.getKindName(card.kind):
                            return trump
                print("trump must exist among your cards.")
            else:
                print("invalid answer. Trump must be a valid card type")

    def printCards(self):
        """ prints the cards using printDeck which prints them
        in rows for them to appealing.
        """
        cards = self.gameData.cards[self.name]
        printDeck(cards)

    def doesExist(self, current_card):
        """ checks if the given card exists in the player's deck.
        If so, it gives its index, otherwise returns -1.
        current_card: the card we want to see if exists.(GameCard)
        """
        # retrieve the list of cards of same suit as current_card
        cards = self.gameData.cards[self.name]\
            [GameCard.getKindName(current_card.kind)]
        for i in range(len(cards)):
            card = cards[i]
            if card == current_card:
                return i
        return -1

    def getCard(self):
        """ asks the user about a card and makes sure the card 
        correctly matches the roles of Court Piece. Keeps asking 
        the user until they return the correct answer, and then 
        it will  return the card. The returned card is removed 
        from the player's deck and is a GameCard object.
        """
        def isItACard(input_):
            """ Checks if the given pair(supposed
            to be a [suit, rank] is a real card or not).
            input_: is a list that represents the input. (list)
            """
            if len(input_) == 2:
                if input_[0] in GameCard.KINDS:
                    if input_[1] in GameCard.RANKS:
                        return True
            return False

        guideline = "Note: first enter the kind followed by " \
                    "comma followed by rank.\n" \
                    "ex: Spade, One         Heart, King"
        # print cards only once.
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
                # construct a card object
                current_card = GameCard(given[0], given[1])
                # does the card actually exist in the player's deck
                ans = self.doesExist(current_card)
                if ans != -1:
                    cards = self.gameData.cards[self.name]
                    # check if the chosen card comply to the game's
                    # rules
                    last_card = self.gameData.table\
                        [self.gameData.last_winner_ind]
                    if last_card is not None:
                        king_kind = GameCard.getKindName(last_card.kind)
                        # if the player has similar card to the
                        # first player but the chosen card is
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
        """ it is the only function that is supposed to be called
            by game handler directly. It would return the response \
            based on the request action.
            action: if "trump" returns the trump of game. if
                    "pick" returns the next playing card.(str)
        """
        if action == "trump":
            if self.gameData.king.name == self.name:
                return self.getTrump()
        elif action == "pick":
            return self.getCard()
