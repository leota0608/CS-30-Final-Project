###############################################################################
#Coder: Leo
#Last date modified: 1/14/2026
###############################################################################
"""This module is the deck code for the mini game EndPhase. It is 
imported by EndPhase.py. The code contains the Deck class."""
###############################################################################
import random


class Deck:
    """This class is the deck of cards in the game.
    The perimeter card_list is a list of cards needed to be made into
    the deck of cards."""
    def __init__(self, card_list):
        self.card_list = card_list
    
    def draw(self, num):
        """This methods draws num cards from the list of cards and 
        returns them. num is the number of cards to be drew."""
        cards_drawn = self.card_list[0:num]
        self.card_list = self.card_list[num:]
        return cards_drawn
    
    def shuffle(self):
        """This class uses shuffle method from random to randomize the 
        deck of cards."""
        random.shuffle(self.card_list)