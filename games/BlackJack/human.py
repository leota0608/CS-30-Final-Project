###############################################################################
#Coder: Leo
#Last date modified: 1/14/2026
###############################################################################
"""This module is the human code for the mini game Black Jack. It is 
imported by BlackJackGame.py. The code contains the Human class."""
###############################################################################
import json
import random
from games.common.Character import Character
from games.common.GameCard import GameCard


class Human(Character):
    """The class inherits from Character class.
    it creates a human object."""
    def __init__(self):
        self.load_current_player_information()
        self.handcard = []
        self.alive = True
        self.sum = []
        self.handcard_display = []

    def add_card(self, name):
        """This method adds a card to the human's handcards.
        name is an integer from 1 to 13(ace-king) and at the same 
        time assign random kinds to it"""
        self.handcard.append(name)
        card = ["ace", "two", "three", "four", "five", "six", "seven", \
                "eight", "nine", "ten", "jack", "queen", "king"]
        name = card[name-1]
        self.handcard_display.append(GameCard(random.choice\
                (["club", "spade", "heart", "diamond"]), name))

    def find_sum(self):
        """Checks the sum of current handcards, both the maximum and minimum 
        sum and stores them"""
        total = 0
        count_a = 0
        for i in self.handcard:
            if i == 1:
                count_a += 1
            elif i > 10:
                total += 10
            else:
                total += i
        self.sum = [total, count_a]
        self.min_sum = total + count_a
        self.max_sum = total
        while count_a > 0:
            if self.max_sum + 11 <= 21:
                self.max_sum += 11
                count_a -= 1
            else:
                break

    def load_current_player_information(self):
        """This method loads the current human player's information 
        from playingRecord.json"""
        try:
            with open("player/playingRecord.json", 'r') as file:
                p = json.load(file)
                self.player_information = p[str(p["Total Player"])]
        except:
            print("**Failed to open playingRecord.json**")

