###############################################################################
# Coder: Leo
# Last date modified: 1/14/2026
###############################################################################
"""This module is the bot module for mini-game EndPhase.
The code is imported by EndPhaseGame.py. It mainly contains the
class Bot, which controls all movement of bot in the game."""
###############################################################################
import json
import random
from games.EndPhase.human import Human


class Bot(Human):
    """This class is inherited from Human class, these are the 
    perimeters:
    name: the name of the bot
    health: the initial health of the bot
    enemy_num: the enemy number that bot has
    index: the index the bot has in the list of players"""
    def __init__(self, name, health, enemy_num, index):
        Human.__init__(self, name, health, index)
        self.enemy_num = enemy_num
        self.enemy = []
        self.card_nums = card_nums
        self.creat_enemies()
        self.alive = True
        self.act_step = 1

    def creat_enemies(self):
        """This method creates the enemies of the bot according to 
        enemy_nums and store it as a dictionary."""
        total_card_nums = 0
        for i, j in self.card_nums.items():
            total_card_nums += j
        for i in range(0, self.enemy_num + 1):
            if str(i + 1) == self.name[-1]:
                self.enemy.append("self")
                continue
            self.enemy.append({"index": i,
                               "alive": True,
                               "health": self.health,
                               "estimated_handcards": self.card_nums.copy(),
                               "equipment": {"weapen": None, "armor": None},
                               "handcard_num": self.health})

    def find_high_value_target(self, player):
        """This method has a player perimeter which is the player list, 
        it then returns the player
        with highest value: with equipment or has lowest health."""
        targets_with_equipment = []
        player_health = []
        for i in range(len(player)):
            if i == self.index or not player[i].alive:
                continue
            if player[i].equipment["weapen"] is not None or player[i]. \
                    equipment["armor"] is not None:
                targets_with_equipment.append(i)
                player_health.append([player[i].health, player[i].index])
            elif len(player[i].handcards) >= 1:
                player_health.append([player[i].health, player[i].index])
        if len(targets_with_equipment) > 0:
            return random.choice(targets_with_equipment)
        player_health.sort(key=lambda x: x[0])
        random_num = random.randint(0, 100)
        if len(player_health) == 0:
            return -1
        if len(player_health) > 1 and random_num <= 40:
            # 40% attack other players
            return player_health[random.randint(1, len(player_health) - 1)][1]
        else:  # 60% chance attack player with lowest health
            return player_health[0][1]

    def take_move(self, player):  # choose the card to play in start phase
        """
        This method is the core strategy of the bot.
        it has a perimeter of list of players.
        After it make decision, it returns the cards object and the index 
        in handcard.
        """
        # select available cards to play from handcards
        available_moves = []
        for i in range(0, len(self.handcards)):
            if not (self.handcards[i].name == "dodge" or \
                    self.handcards[i].name == "negate"):
                # card_name, index
                available_moves.append([self.handcards[i], i])
        # basic rules
        ## 1. if have peach and health is not full, use peach
        if self.health < self.max_health:
            for i in available_moves:
                if i[0].name == "peach":
                    return {"card": self.handcards[i[1]], "target": -1, \
                            "index": i[1]}
        ## 2.
        equipment = []
        for i in available_moves:
            if i[0].type == "equipment":
                equipment.append(i)
        # weapen rank according to importance
        count_slash = 0
        for i in available_moves:
            if i[0].name == "slash":
                count_slash += 1
        if count_slash >= 2 or self.health <= 3:
            weapen_rank = ["crossblade", "crossbow"]
        else:
            weapen_rank = ["crossbow", "crossblade"]
        for i in weapen_rank:
            for j in equipment:
                if i == j[0].name:
                    if (self.equipment["weapen"] is not None and j[0].name \
                        != self.equipment["weapen"].name) or \
                            len(self.handcards) > self.max_handcards:
                        return {"card": self.handcards[j[1]], "target": -1, \
                                "index": j[1]}  # equip the best weapen
        # armor rank according to importance
        armor_rank = ["evasion"]
        for i in armor_rank:
            for j in equipment:
                if i == j[0].name:
                    if (self.equipment["armor"] is not None and j[0].name \
                        != self.equipment["armor"].name) or \
                        len(self.handcards) > self.max_handcards:
                        return {"card": self.handcards[j[1]], "target": -1, \
                                "index": j[1]}
        ## 3.
        # AOE and self beneficial cards
        trick_cards = ["savage", "archery", "benevolence"]
        for i in available_moves:
            if i[0].name in trick_cards:
                return {"card": self.handcards[i[1]], "target": -1, \
                        "index": i[1]}
        ## 4.
        # dismantle and snatch
        target = self.find_high_value_target(player)
        if target != -1 and (len(player[target].handcards) > 0 or \
                             player[target].equipment["weapen"] \
                             is not None or not player[target]. \
                                        equipment["armor"] is None):
            trick_cards = ["snatch", "dismantle"]
            for j in trick_cards:
                for i in available_moves:
                    if i[0].name == j:
                        return {"card": self.handcards[i[1]], \
                                "target": target, "index": i[1]}
        ## 5. 
        # duel
        count_slash = 0
        for i in available_moves:
            if i[0].name == "slash":
                count_slash += 1
        if count_slash >= 1 and self.health >= 3 or (count_slash >= 2 \
                                                     and self.health >= 2):
            for i in available_moves:
                if i[0].name == "duel":
                    target = self.choose_target()
                    if len(target) == 1 or random.randint(0, 100) < 50:
                        return {"card": self.handcards[i[1]], \
                                "target": target[0][1], "index": i[1]}
                    else:
                        target = target[random.randint(1, len(target) - 1)]
                        return {"card": self.handcards[i[1]], \
                                "target": target[1], "index": i[1]}
        if len(self.handcards) <= self.max_handcards and self.health <= 2:
            return -1
        # play slash
        if self.act_step == 1:
            self.act_step -= 1
            for i in available_moves:
                if i[0].name == "slash":
                    target = self.choose_target()
                    if len(target) == 1 or random.randint(0, 100) < 50:
                        return {"card": self.handcards[i[1]], "target":
                            target[0][1], "index": i[1]}
                    else:
                        target = target[random.randint(1, len(target) - 1)]
                        return {"card": self.handcards[i[1]], "target":
                            target[1], "index": i[1]}
        return -1

    def choose_target(self):
        """This method returns the player list sorted according health 
        in ascending order"""
        target = []
        for e in self.enemy:
            if e == "self" or not e["alive"]:
                continue
            target.append([e["health"], e["index"]])
        target.sort(key=lambda x: x[0])
        return target

    def discard_card(self):
        """This methods lets the bot discard cards according to 
        their value.
        else it returns a random card index"""
        for i in range(0, len(self.handcards)):
            if self.handcards[i].name == "duel":
                return i
        for i in range(0, len(self.handcards)):
            if self.handcards[i].name == "slash":
                return i
        for i in range(0, len(self.handcards)):
            if self.handcards[i].name == "dodge":
                return i
        for i in range(0, len(self.handcards)):
            if self.handcards[i].name == "peach":
                return i
        return random.randint(0, len(self.handcards) - 1)


# this code opens card.json stores the card and card_nums dictionary
try:
    with open("games/EndPhase/card.json", 'r') as file:
        content = json.load(file)
        card = content["card"]
        card_nums = content["card nums"]
except FileNotFoundError:
    print("Failed to locate card.json")
except:
    print("Failed to open card.json for some unknown reason")