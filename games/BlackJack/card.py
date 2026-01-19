###############################################################################
# Coder: Leo
# Last date modified: 1/14/2026
###############################################################################
"""This module is the card code for the mini game Black Jack. It is 
imported by BlackJackGame.py. The code contains the Card class.
The class contains the card name of cards"""


###############################################################################
class Card:
    """The card method, having the variable self.name, 
    belongs to deck list, which is a list of card objects"""

    def __init__(self, name):
        self.name = name
