class Human:
    def __init__(self, name, health):
        self.initial_health = health
        self.name = name
        self.health = health
        self.handcards = []
        self.equipment = {"weapen": None, "armor": None}
        self.max_handcards = health
        self.alive = True
    
    def add_handcards(self, new_handcards):
        self.handcards.extend(new_handcards)