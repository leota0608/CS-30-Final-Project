import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import json
from games.common.Character import Character


class Human(Character):
    def __init__(self):
        self.load_current_player_information()
        self.handcard = []
        self.alive = True
        self.sum = []

    def add_card(self, name):
        self.handcard.append(name)

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

    def load_current_player_information(self):
        try:
            with open("player/playingRecord.json", 'r') as file:
                p = json.load(file)
                self.player_information = p[str(p["Total Player"])]
        except:
            print("**Unable to open playingRecord.json**")

