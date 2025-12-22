import random
class Deck:
    def __init__(self, card_list):
        self.card_list = card_list
    
    def draw(self, num):
        cards_drawn = self.card_list[0:num]
        self.card_list = self.card_list[num:]
        return cards_drawn
    
    def shuffle(self):
        random.shuffle(self.card_list)