###############################################################################
# Coder: Leo
# Last date modified: 1/14/2026
###############################################################################
"""This module is the card code for the mini game EndPhase. It is 
imported by EndPhase.py. The code contains the Card class."""
###############################################################################
class Card:
    """This class has two perimeters:
    name: the name of the card object
    type: the type of the card object"""
    def __init__(self, name, type):
        self.name = name
        self.type = type
