from games.common.Character import Character
import random

from games.common.GameCard import GameCard

class Bot(Character):
    def __init__(self):
        self.handcard = []
        self.alive = True
        self.sum = []
        self.handcard_display = []


    def add_card(self, name):
        self.handcard.append(name)
        card = ["ace", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "jack", "queen", "king"]
        name = card[name-1]
        self.handcard_display.append(GameCard(random.choice(["club", "spade", "heart", "diamond"]), name))

    def find_sum(self):
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
        # the unused variables are for future improvements on evaluating methods
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


            
