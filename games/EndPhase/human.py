###############################################################################
#Coder: Leo
#Last date modified: 1/14/2026
###############################################################################
"""This module is the human code for the mini game EndPhase. It is 
imported by EndPhase.py. The code contains the Human class."""
###############################################################################
from games.common.Character import Character


class Human(Character):
    """The class inherits form Character class, which includes
    user name and game data. It has following perimeters:
    name: human player name
    health: initial health of player
    index: the index of the player(0)
    """
    def __init__(self, name, health, index):
        self.initial_health = health
        self.name = name
        self.health = health
        self.handcards = []
        self.equipment = {"weapen": None, "armor": None}
        self.max_handcards = health
        self.alive = True
        self.max_health = health
        self.index = index
    
    def add_handcards(self, new_handcards):
        """
        This method add a list of handcards to the current 
        handcard list"""
        self.handcards.extend(new_handcards)