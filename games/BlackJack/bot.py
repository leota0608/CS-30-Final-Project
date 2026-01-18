###############################################################################
#Coder: Leo
#Last date modified: 1/14/2026
###############################################################################
"""This module is the bot code for the mini game Black Jack. It is 
imported by BlackJackGame.py. The code contains the Bot class.
The class controls all movements of the bot in the game"""
###############################################################################
from games.common.Character import Character
from games.common.GameCard import GameCard
import random


class Bot(Character):
    """This is the bot method that evaluate all bot moves in the game 
    Black Jack. It inherits from CHaracter class. It includes the 
    strategy of whether or not the robot choose to draw a card."""
    def __init__(self):
        self.handcard = []
        self.alive = True
        self.sum = []
        self.handcard_display = []

    def add_card(self, name):
        """This method adds a card to the robots handcard.
        name if the perimeter which is an integer from 1 to 13 
        (ace to king)"""
        self.handcard.append(name)
        card = ["ace", "two", "three", "four", "five", "six", "seven",\
                 "eight", "nine", "ten", "jack", "queen", "king"]
        name = card[name-1]
        self.handcard_display.append(GameCard(random.choice(["club", \
                                "spade", "heart", "diamond"]), name))

    def find_sum(self):
        """This method checks the maximum and minimum 
        sum the bot already has(count 1 as in 11 and 1) 
        and store them in self.max_sum and self.min_sum"""
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

    def evaluate_draw(self, human_draw, player_list, deck, index):
        """This methods evaluates the move of the robot of 
        choosing whether to draw.
        Perimeter explanations:
        human_draw: a boolean value indicating did the 
        human player draw in his round
        player_list: the list of player objects
        deck: the deck of remaining cards
        index: the bot's index in the list
        The method returns true or false indicating 
        to draw or not to draw
        """
        # the unused perimeters are for future improvements on evaluating 
        # methods
        player_alive = 0
        for i in player_list:
            if i.alive:
                player_alive += 1
        if player_alive <= 2:
            if self.max_sum < player_list[0].max_sum:
                return True
            else:
                return False
        choice = random.randint(1,10)
        if choice <= 2:
            return True # 20% chance to draw no matter what
        if self.max_sum > player_list[0].max_sum:
            if self.max_sum >= 17:
                return False
            else:
                return True
        else:
            if self.max_sum <= 15:
                return True
            else:
                min_score = 666
                min_index = 0
                for i in range(0, len(player_list)):
                    if player_list[i].max_sum < min_score:
                        min_score = player_list[i].max_sum
                        min_index = i
                if min_index == index:
                    return True
                return False