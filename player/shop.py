import json
import time
import random
from games.EndPhase.choose import choose
class Shop:
    def __init__(self, player):
        self.player = player
        with open("player/bodyParts.json", 'r') as content:
                data = json.load(content)
                self.bodyParts = data["bodyParts"]
                self.prices = data["prices"]
                self.probability = data["probability"]
        self.items = []
            
    def refresh_store_items(self):
        self.items = []
        for i in range(0, len(self.bodyParts)):
            if random.choice([0, 1]) == 1:
                self.items.append(self.bodyParts[i])
        
    
    def print_shop(self):
        print("**Shop**")
        if len(self.items) == 0:
            print("There are no body parts available right now!")
        else:
            print("Available body parts:")
            for i in range(len(self.items)):
                print(f"{i+1}. {self.items[i]} (${self.prices[self.items[i]]})", end='')
                if self.items[i] in self.player.lost_body_part:
                    print("-Lost-")
                else:
                    print("")
        print(f"{len(self.items)+1}. Leave")
        return len(self.items) + 1

    def buy(self):
        self.refresh_store_items()
        skip = False
        while True:
            if not skip:
                item_num = self.print_shop() # put missing next to the missing body parts
                valid_choices = []
                for j in range(item_num):
                    valid_choices.append(str(j+1))
            item_choice = int(choose(f"What do you want to buy?(Current money: ${self.player.money})", valid_choices, "yes"))
            
            if item_choice == item_num: # leave
                print("You left the shop")
                time.sleep(0.7)
                return
            body_part = self.items[item_choice-1]
            if not body_part in self.player.lost_body_parts:
                print(f"You already have {body_part}")
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

            
    