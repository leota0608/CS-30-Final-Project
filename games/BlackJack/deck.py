import random
class Deck:
    def __init__(self):
        self.card_list = []
        self.remaining = 52

    def initialise(self):
        for i in range(1, 14):
            for j in range(4):
                self.card_list.append(i)
    
    def shuffle(self):
        random.shuffle(self.card_list)
        
    def draw(self):
        self.remaining -= 1
        if self.remaining < 0:
            print("**Error: remaining deck of cards < 0 (game2-deck)**")
        return self.card_list.pop()