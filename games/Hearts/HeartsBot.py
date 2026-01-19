###############################################################################
# Coder: Amir
# Last date modified: 1/14/2026
###############################################################################
""" Creates the logic for the computer player and wraps it within the
 outlined design structure of the Character class."""
###############################################################################
import random as rd
from games.common.Character import Character
from games.common.GameCard import GameCard


class HeartsBot(Character):
    """ HeartsBot defines the bot for the game of hearts. It follows
    a simple algorithm to come up with the best option to play.
    Here is a flowchart sudo-code like structure of this algorithm.

    # card exchange phase:
    Note: Three cards must be chosen for exchange.
    - if queen of spade is among the cards choose it for change.
    - Pick as many hearts as possible for change.
    - If you have not picked enough cards yet, pick random cards
      out of the deck.

    # play phase:
    - if we are the first player:
        - check if we can play the queen of spade (it means that if 
        we play queen of spade, there is at least one player with a 
        higher rank, ex: king of spade.) In that case play the queen 
        of spade.
        - Otherwise check if we can play a heart. (At least someone 
        must have higher rank than our least heart rank.) In this case 
        play a heart.
        - Otherwise pick a random card, prioritizing, club and diamond
        over spade and heart.
    - if we are a middle player(just not the first):
        - if we have the same suit as the first player, then pick the 
        smallest rank and put on the table.
        - Otherwise pick a random card, prioritising, heart and the 
        queen of spade, over club, diamond and other cards of spade.
    """
    def __init__(self, name):
        """ name: the name of bot.(string)
        """
        super().__init__(name)

    def pickRandomCard(self):
        """ Chooses any random card from player's deck
        and returns it.
        """
        suits = []
        # player's deck is not in the Bot class
        # it is in the gameData class that is globally
        # shared.
        cards = self.gameData.cards[self.name]
        # creating a list of suits to choose randomly
        # from.
        for suit in cards:
            if len(cards[suit]) != 0:
                suits.append(suit)
        # pick random suit and then random card
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
        # list of cards removed
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
        # removing cards in pop_list
        for pop_ in range(len(pop_list) - 1, -1, -1):
            cards["heart"].pop(pop_)
        # putting the remaining cards randomly.
        while len(exchange_cards) < 3:
            exchange_cards.append(self.pickRandomCard())
        return exchange_cards

    def isTableEmpty(self):
        """ table is a list of cards that represents the current
        played cards. If it is empty it means that no one has played
        anything and if it is our turn it implies we are first player.
        """
        for item in self.gameData.table:
            if item is not None:
                return False
        return True

    def findSmallestCard(self, suit, player):
        """ finds the smallest of cards of specific suit.
        suit: the suit of the card.(str)
        player: player's name.(str)
        """
        cards = self.gameData.cards[player][suit]
        # the index of the smallest card
        which = 0
        if len(cards) != 0:
            for i in range(len(cards)):
                if cards[which].rank > cards[i].rank:
                    which = i
            # return the index of the smallest card.
            return which
        else:
            return -1

    def canPlayHeart(self):
        """ if at least one player has a heart
        card that is larger than the smallest heart
        card that we have, then it is the wisest to play heart.
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
                    if sRank > rank:
                        return lowest_heart
        return -1

    def canPlaySpadeQueen(self):
        """
        checks if we can play the spade queen.
        It returns the index of the queen of spade
        if it can be played, otherwise returns -1.
        """
        cards = self.gameData.cards[self.name]["spade"]
        # checking if we have any spade
        if len(cards) != 0:
            found = -1
            # checking if we have queen of spade
            for i in range(len(cards)):
                card = cards[i]
                if card == GameCard("spade", "queen"):
                    found = i
                    break
                # check if any player has a higher rank than
                # queen of spade, and it is their minium rank.
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
        # player cards retrieved from gameData
        cards = self.gameData.cards[self.name]
        # list of diamonds and clubs
        da = []
        for suit in ["diamond", "club"]:
            if len(cards[suit]) != 0:
                da.append(suit)
        # if we have at least one of diamond or club
        # we choose a random card out of them
        if len(da) != 0:
            chosen = rd.choice(da)
            ind = self.findSmallestCard(chosen, self.name)
            return cards[chosen].pop(ind)
        else:
            ind = self.findSmallestCard("spade", self.name)
            if ind != -1:
                rank = cards["spade"][ind].rank
                # if the smallest rank of spade in our deck
                # is spade of queen and that no hearts
                # exist the wisest is to draw the queen.
                if rank == GameCard.RANKS["queen"]:
                    if len(cards["heart"]) == 0:
                        return cards["spade"].pop(ind)
                    else:
                        ind = self.findSmallestCard("heart", self.name)
                        if ind != -1:
                            return cards["heart"].pop(ind)
                else:
                    # there must be at least one card in the spades
                    rd.shuffle(cards["spade"])
                    return cards["spade"].pop()
            else:
                # there must be at least one card in the hearts
                ind = self.findSmallestCard("heart", self.name)
                return cards["heart"].pop(ind)

    def getUnSuitCard(self):
        """
        In the case were we do not have the suit card,
        we should play a different card. It is best
        to play a queen spade, a heart, if possible.
        """
        # retrieve current player's cards.
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
        # since no heart existed we go with heart club and spade.
        # Note: earlier we realized that queen of spade does not exist
        # but other spade cards are of course possible.
        # it is best to prioritize diamond and club, but
        # here we just dumb down the computer player a bit.
        da = []
        for suit in ["diamond", "club", "spade"]:
            if len(cards[suit]) != 0:
                da.append(suit)
        chosen = rd.choice(da)
        rd.shuffle(cards[chosen])
        return cards[chosen].pop()

    def choosePlayCard(self):
        """ Chooses a playing card by putting all the top functions
        together. See the sudo-code in the top for more info on
        how the logic works.
        """
        if self.isTableEmpty():     # table empty, we are first player
            # prioritize heart and queen of spade.
            # deliberately choose heart first to dumb down the
            # robot a little.
            ans = self.canPlayHeart()
            if ans != -1:
                return self.gameData.cards[self.name]["heart"].pop(ans)
            ans = self.canPlaySpadeQueen()
            if ans != -1:
                return self.gameData.cards[self.name]["spade"].pop(ans)
            return self.getPrioCard()
        else:
            # get the suit of the game also known as king kind.
            suit = GameCard.getKindName(self.gameData.
                            table[self.gameData.starter_player].kind)
            # retrieve current player's cards
            cards = self.gameData.cards[self.name]
            if len(cards[suit]) != 0:
                ind = self.findSmallestCard(suit, self.name)
                return cards[suit].pop(ind)
            else:
                # we do not have the king kind, play another card.
                return self.getUnSuitCard()

    def provoke(self, action):
        """ the only function called by game handler.
        action: either exchange, if you want the bot to compute its
        exchange cards, or "play" for the bot to choose a card
        to play.(str)
        """
        if action == "exchange":
            return self.getCardsToExchange()
        elif action == "play":
            return self.choosePlayCard()
