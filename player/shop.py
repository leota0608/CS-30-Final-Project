import json
import random
class Shop:
    def __init__(self, player):
        self.player = player
        with open("games/player/bodyParts.json", 'r') as content:
                data = json.load(content)
                self.bodyParts = data["bodyParts"]
                self.probability = data["probability"]
        self.items = []
            
    def refresh_store_items(self, displayed_num):
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
                print(f"- {self.items[i]}")