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
        self.alive = True
        self.act_step = 1

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
        for i in range(0, self.enemy_num+1):
            if str(i+1) == self.name[-1]:
                self.enemy.append("self")
                continue
            self.enemy.append({"index": i,
                               "alive": True,
                               "health": self.health, 
                               "estimated_handcards": self.card_nums.copy(), 
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

    def take_move(self):# choose the card to play in start phase
        # select available cards to play from handcards
        available_moves = []
        for i in range(0, len(self.handcards)):
            if not self.handcards[i].name == "dodge" or self.handcards[i].name == "negate":
                available_moves.append([self.handcards[i], i])# card_name, index
        # basic rules
        ## 1.
        if self.health < self.max_health: # if have peach and health is not full, use peach
            for i in available_moves:
                if i[0].name == "peach":
                    return {"card": self.handcards[i[1]], "target": -1, "index": i[1]}
        ## 2.
        equipment = []
        for i in available_moves:
            if i[0].type == "equipment":
                equipment.append(i)
        # weapen rank according to importance
        weapen_rank = ["crossbow", "crossblade"]
        for i in weapen_rank:
            for j in equipment:
                if i == j[0].name:
                    return {"card": self.handcards[j[1]], "target": -1, "index": j[1]} # equip the best weapen
        ## 3.
        #temp
        if self.act_step == 1:
            self.act_step -= 1
            for i in available_moves:
                if i[0].name == "slash":
                    target = []
                    for e in self.enemy:
                        if e == "self" or not e["alive"]:
                            continue
                        target.append([e["health"], e["index"]])
                    target.sort(key=lambda x: x[0])
                    return {"card": self.handcards[i[1]], "target": target[0][1], "index": i[1]}
        
        return -1
                
            
    # update enemy in main