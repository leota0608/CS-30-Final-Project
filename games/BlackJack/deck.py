import random


class Deck:
    """This method creates a deck of cards, 52 cards, 4*1-13"""
    def __init__(self):
        self.card_list = []
        self.remaining = 52

    def initialise(self):
        # initialising the deck of cards
        for i in range(1, 14):
            for j in range(4):
                self.card_list.append(i)
    
    def shuffle(self):
        """Using random's shuffle method to randomize the list"""
        random.shuffle(self.card_list)
        
    def draw(self):
        """draws a card. The method returns the last element of the card list and removes it."""
        self.remaining -= 1
        if self.remaining < 0:
            print("**Error: remaining deck of cards < 0 (game2-deck)**")
        return self.card_list.pop()