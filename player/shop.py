###############################################################################
# Coder: Leo
# Last date modified: 1/14/2026
###############################################################################
"""This module is the shop module. It contains the Shop class, 
which sells lost body parts to the player."""
###############################################################################
import json
import time
import random
from games.EndPhase.choose import choose


class Shop:
    """This class is the Shop class, it is imported by main.py
    It displays a random selection of body parts to the player, 
    and labels chich ones the player is missing."""

    def __init__(self, player):
        self.player = player
        try:
            with open("player/PlayerStarterData.json", 'r') as content:
                data = json.load(content)
                self.bodyParts = data["bodyParts"]
                self.prices = data["prices"]
                self.probability = data["probability"]
        except:
            print("Failed to open PlayerStarterData.json")
        self.items = []

    def refresh_store_items(self):
        """This method refreshes the items in the store"""
        self.items = []
        for i in range(0, len(self.bodyParts)):
            if random.choice([0, 1]) == 1:
                self.items.append(self.bodyParts[i])

    def print_shop(self):
        """This method prints the shop and bodyparts for 
        the player to see"""
        print("**Shop**")
        if len(self.items) == 0:
            print("There are no body parts available right now!")
        else:
            print("Available body parts:")
            for i in range(len(self.items)):
                print(f"{i + 1}. {self.items[i]} "
                      f"(${self.prices[self.items[i]]})", end='')
                if self.items[i] in self.player.lost_body_parts:
                    print("-Lost-")
                else:
                    print("")
        print(f"{len(self.items) + 1}. Leave")
        return len(self.items) + 1

    def buy(self):
        """This method is called when the player enter the shop,
        it checks if the player has enough money to buy the body
        part he selected."""
        self.refresh_store_items()
        skip = False
        while True:
            if not skip:
                # put missing next to the missing body parts
                item_num = self.print_shop()
                valid_choices = []
                for j in range(item_num):
                    valid_choices.append(str(j + 1))
            item_choice = int(choose(f"What do you want to buy?"
                                     f"(Current money: ${self.player.money})",
                                     valid_choices, "yes"))
            if item_choice == item_num:  # leave
                print("You left the shop")
                time.sleep(0.7)
                return
            body_part = self.items[item_choice - 1]
            if not body_part in self.player.lost_body_parts:
                print()
                print("you bastard!")
                print("check what you have and what you do not " \
                      "have before coming here.")
                print(f"You already have {body_part}")
                print()
            elif self.player.money >= self.prices[body_part]:
                # buy
                self.player.money -= self.prices[body_part]
                print(f"{body_part} successfully attatched to your body...")
                time.sleep(0.7)
                self.player.gain(body_part)
                self.items.remove(body_part)
            else:
                print("Your money is not enough...")
                skip = True
