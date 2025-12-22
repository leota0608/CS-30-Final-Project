import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
import json
from games.game1.human import Human 

with open("games/game1/card.json", 'r') as file:
    content = json.load(file)
    card = content["card"]
    card_nums = content["card nums"]

class Bot(Human):
    def __init__(self, name, health, enemy_num):
        Human.__init__(self, name, health)
        self.enemy_num = enemy_num
        self.enemy = []
        self.card_nums = card_nums
        self.creat_enemies()

    def evaluate_cardnums(self, card_nums):
        self.card_nums = card_nums

    def update_cardnums(self, card_name, change):
        self.card_nums[card_name] += change
        if self.card_nums[card_name] < 0:
            print("**ERROR: Wrong card numbers**")

    def creat_enemies(self):
        total_card_nums = 0
        for i, j in self.card_nums.items():
            total_card_nums += j
        for i in range(0, self.enemy_num):
            if str(i+1) == self.name[-1]:
                self.enemy.append("self")
                continue
            self.enemy.append({"enemy_index": i,
                               "health": self.health, 
                               "estimated_handcards": self.card_nums, 
                               "equipment": {"weapen": None, "armor": None},
                               "handcard_num": self.health})
    
    def update_total_cardnums(self):
        num = 0
        for i, j in self.card_nums.items():
            num += j
        self.total_cardnums = num
        
    def evaluate_slash(self):
        score = []
        for i in self.enemy:
            score.append((self.initial_health/self.health)*(10/100)) # 10%
            opp_dodge_num = (self.card_nums["dodge"]-self.handcards["dodge"])/(self.total_cardnums-self.handcards["dodge"]) * len(i.handcards) # estimated opponent dodge number
            self_slash_num = self.handcards["slash"]

    def take_move(self):# choose the card to play
        available_moves = []
        for i in range(0, len(self.handcards)):
            evaluate_card = self.handcards[i]
            if evaluate_card.type == "basic":
                if evaluate_card.name == "slash":
                    available_moves.append(self.evaluate_slash())

    # update enemy in main