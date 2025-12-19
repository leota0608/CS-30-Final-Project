"""
This is just an illustration of how to use
the GameHandler and Character classes correctly
and efficiently.
"""
from GameHandler import GameHandler
from character import Character
import random

class Player:
    def __init__(self):
        self.name = ""
        self.age = 0

    def getName(self):
        self.name = input("What is your name? ")
    
    def getAge(self):
        self.age = int(input("What is your age? "))


class GameData:
    def __init__(self):
        self.choices = ["rock", "paper", "scissor"]


class Bot(Character):
    def provoke(self):
        return random.choice(self.gameData.choices)
    
    def sendMessage(self):
        return random.choice([None, "I will win you!", "Damn", "Loser", "I'll Win, I'll win!"])


class HumanRPSPlayer(Character):

    def __init__(self, player):
        self.player = player

    def provoke(self):
        return input("Rock Paper Scissor, Shhoooot> ").lower()
    
    def sendMessage(self):
        return None
    
class RPSGame(GameHandler):
    def __init__(self, characters, runs):
        GameHandler.__init__(self, characters, GameData())
        self.runs = runs

    def run(self):
        print("Welocme everyone to RPS(Rock Paper Scissor) Shoot party")
        print(f"You will play {self.runs} turns")
        for i in range(self.runs):
            human = self.character[0].provoke()
            computer = self.character[1].provoke()

    
