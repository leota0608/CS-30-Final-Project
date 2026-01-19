""" This is just an illustration of how to use
the GameHandler and Character classes, correctly
and efficiently.
The example uses Rock Paper Scissor Shoot game
for this purpose.
"""
from GameHandler import GameHandler
from Character import Character
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

    def provoke(self, action):
        return random.choice(self.gameData.choices)


class HumanRPSPlayer(Character):
    def __init__(self, player, name):
        super().__init__(name)
        self.player = player

    def provoke(self, action):
        return input("Rock Paper Scissor, Shoot> ").lower()


class RPSGame(GameHandler):
    def __init__(self, characters, runs):
        GameHandler.__init__(self, characters, GameData())
        self.runs = runs

    def run(self):
        print("Welcome everyone to RPS(Rock Paper Scissor Shoot) party")
        print(f"You will play {self.runs} turns")
        for i in range(self.runs):
            human = self.characters[0].provoke(None)
            computer = self.characters[1].provoke(None)
            print(f"computer says {computer}")
            if human == computer:
                print("it is a tie")
            elif human == "rock":
                if computer == "paper":
                    print("oh, computer won.")
                else:
                    print("yah, you won.")
            elif human == "scissor":
                if computer == "paper":
                    print("oh, you beat the computer.")
                else:
                    print("no, computer won.")
            elif human == "paper":
                if computer == "rock":
                    print("let's go, computer lost.")
                else:
                    print("you lost.")


playerInfo = Player()
playerInfo.getName()
playerInfo.getAge()

computer = Bot("batman")
human = HumanRPSPlayer(playerInfo, "amir")

game = RPSGame([human, computer], 5)
game.run()
